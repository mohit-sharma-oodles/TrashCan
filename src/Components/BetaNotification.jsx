import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {useRoute} from '@react-navigation/native';
import {useTranslation} from 'react-i18next';

const BetaNotification = () => {
  const {t} = useTranslation();
  const route = useRoute();
  // console.log(route.name);
  return (
    <View style={{backgroundColor: 'lightgray', padding: 16, marginBottom: 48}}>
      <Text>{t('betaNotification.message', {routeName: route.name})}</Text>
    </View>
  );
};

export default BetaNotification;

const styles = StyleSheet.create({});
