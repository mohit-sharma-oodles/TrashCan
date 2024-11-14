import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import BetaNotification from '../../Components/BetaNotification';

const HomeScreen = () => {
  return (
    <View style={{flex: 1, justifyContent: 'space-between'}}>
      <Text>HomeScreen</Text>
      <BetaNotification />
    </View>
  );
};

export default HomeScreen;

const styles = StyleSheet.create({});
