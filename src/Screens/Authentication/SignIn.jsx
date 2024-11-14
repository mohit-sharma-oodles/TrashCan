import {Button, Image, StyleSheet, Text, TextInput, View} from 'react-native';
import React, {useContext} from 'react';
import userContext from '../../Context/userContext';
import {useTranslation} from 'react-i18next';

const SignIn = () => {
  const {user, setUser} = useContext(userContext);
  const {t} = useTranslation();

  return (
    <View style={styles.container}>
      <Image source={require('../../../Assets/Logo.jpg')} style={styles.logo} />
      <View style={styles.formContainer}>
        <TextInput
          style={styles.input}
          placeholder={t('Identifier')}
          name="username"
        />
        <TextInput
          style={styles.input}
          placeholder={t('Password')}
          secureTextEntry={true}
          name="password"
        />
      </View>
      <Button
        title={user ? 'Log Out' : 'Log In'}
        onPress={() => setUser(true)}
      />
    </View>
  );
};

export default SignIn;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: 'white',
    width: '100%',
  },
  formContainer: {
    width: '100%',
    alignItems: 'center',
    marginTop: 20,
  },
  input: {
    height: 40,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    marginVertical: 8,
    width: '90%',
  },
  logo: {
    width: 300,
    height: 300,
    marginTop: 80,
    resizeMode: 'contain',
  },
});
