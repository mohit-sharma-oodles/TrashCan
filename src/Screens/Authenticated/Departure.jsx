import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import BetaNotification from '../../Components/BetaNotification';

const Departure = () => {
  return (
    <View style={{flex: 1, justifyContent: 'space-between'}}>
      <Text>Departure</Text>
      <BetaNotification />
    </View>
  );
};

export default Departure;

const styles = StyleSheet.create({});
