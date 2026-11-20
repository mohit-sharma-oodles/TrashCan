#!/usr/bin/env python3
import socket, ssl, json, time, base64, urllib.request, urllib.error

OUT={}
def log(o):
    print(json.dumps(o)[:900], flush=True)

def http(url, method="GET", body=None, headers=None, timeout=8, auth=None, host=None, insecure=True):
    h={"User-Agent":"Mozilla/5.0","Accept":"*/*"}
    if headers: h.update(headers)
    if host: h["Host"]=host
    if auth: h["Authorization"]="Basic "+base64.b64encode(("%s:%s"%auth).encode()).decode()
    data=body.encode() if isinstance(body,str) else body
    req=urllib.request.Request(url,data=data,method=method,headers=h)
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    t0=time.time()
    try:
        r=urllib.request.urlopen(req,timeout=timeout,context=ctx); b=r.read(6000); st=r.status; hd=dict(r.headers)
    except urllib.error.HTTPError as e:
        st=e.code
        try: b=e.read(6000)
        except Exception: b=b""
        hd=dict(e.headers or {})
    except Exception as e:
        log({"url":url,"host":host,"err":str(e)[:200],"ms":int((time.time()-t0)*1000)}); return None
    o={"url":url,"host":host,"status":st,"len":len(b),"ms":int((time.time()-t0)*1000)}
    for k in ("Server","WWW-Authenticate","Location","Content-Type","X-Powered-By"):
        if k in hd: o[k]=hd[k][:200]
    o["body"]=b.decode("utf-8","replace")[:900]
    log(o); return {"status":st,"body":b,"headers":hd}

def cert(host,port=443,servername=None):
    try:
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        s=ctx.wrap_socket(socket.create_connection((host,port),timeout=8),server_hostname=servername or host)
        c=s.getpeercert(binary_form=False)
        log({"tls":host,"port":port,"sni":servername,"cert":str(c.get("subject"))[:300],"san":c.get("subjectAltName")})
        s.close()
    except Exception as e:
        log({"tls":host,"port":port,"sni":servername,"err":str(e)[:200]})

def tcp(host,port,wait=4):
    try:
        s=socket.create_connection((host,port),timeout=wait); s.settimeout(3)
        try: b=s.recv(200)
        except Exception: b=b""
        log({"tcp":host,"port":port,"open":True,"banner":b.decode("utf-8","replace")[:150]}); s.close()
    except Exception as e:
        log({"tcp":host,"port":port,"open":False,"err":str(e)[:80]})

# 1) OVH managed DB DNS names
for name in ("mysql-f36fd8af-o5a53be78.database.cloud.ovh.net","mysql-3936055b-o5a53be78.database.cloud.ovh.net","mysql-3936055b-o5a53be78.database.cloud.ovh.com"):
    try:
        ips=sorted({x[4][0] for x in socket.getaddrinfo(name,20184,proto=socket.IPPROTO_TCP)})
    except Exception as e:
        log({"dns":name,"err":str(e)[:120]}); continue
    log({"dns":name,"ips":ips})
    for ip in ips:
        tcp(ip,20184); tcp(ip,3306)

# 2) http planes
H="135.125.168.26"
for base,host in [("https://135.125.168.26","machine.credebt.com"),("https://135.125.168.26","135.125.168.26")]:
    for p in ["/","/robots.txt","/.env","/api/health","/dashboard/metabase-dashboard-url","/auth/me","/entity","/asset","/swagger","/swagger-ui/index.html","/v3/api-docs","/api-docs","/actuator/health","/login","/admin","/assets/config.json","/config.json","/main.js"]:
        http(base+p, host=host, timeout=7)
for p in ["/","/health","/api/health","/dashboard/metabase-dashboard-url","/auth/me","/admin","/actuator/health"]:
    http("http://135.125.168.26:3000"+p, host="machine.credebt.com", timeout=7)
    http("http://135.125.168.26:3001"+p, host="machine.credebt.com", timeout=7)

# 3) staging/dev machine 141.95.77.132
S="141.95.77.132"
for host in ("stage-api-machine.credebt.com","machine.credebt.com","api-machine.credebt.com",None):
    http("http://141.95.77.132/swagger/index.html", host=host, timeout=7)
    http("http://141.95.77.132/health", host=host, timeout=7)
http("http://141.95.77.132/swagger/v1/swagger.json", auth=("credebt-swagger","vWyMdNFcbTxg"), timeout=8)
http("https://141.95.77.132/swagger/v1/swagger.json", auth=("credebt-swagger","vWyMdNFcbTxg"), timeout=8)
http("https://141.95.77.132/api/health", timeout=7)
http("https://141.95.77.132/entity", timeout=7)
http("https://141.95.77.132/", timeout=7)
cert(S)

# 4) 162.19.223.4
T="162.19.223.4"
for p in ["/","/health","/api","/api/","/api/v1","/api/v1/","/admin","/admin/","/swagger","/docs","/static/","/robots.txt","/.env","/api/health","/api/v1/health","/status","/login","/metrics"]:
    http("http://162.19.223.4"+p, host="api.credebtmarkets.com", timeout=6)
cert(T)

# 5) TLS certs for the rest
for h in ("135.125.168.26","141.95.77.132","162.19.223.4","51.195.99.241"):
    cert(h)
open("/tmp/i165296_result2.json","w").write(json.dumps(OUT))
