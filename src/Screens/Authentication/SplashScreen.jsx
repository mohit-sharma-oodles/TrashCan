import {Image, StyleSheet, Text, View, StatusBar} from 'react-native';
import React, {useEffect} from 'react';
import {useNavigation} from '@react-navigation/native';

const SplashScreen = () => {
  const navigation = useNavigation();

  useEffect(() => {
    setTimeout(() => {
      navigation.navigate('SignIn');
    }, 2000);
  }, []);

  return (
    <View style={styles.container}>
      <Image source={require('../../../Assets/Logo.jpg')} style={styles.logo} />
    </View>
  );
};

export default SplashScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
  },
  logo: {
    width: 200, // adjust the width to your needs
    height: 200, // adjust the height to your needs
    resizeMode: 'contain', // keeps the aspect ratio of the image
  },
});
