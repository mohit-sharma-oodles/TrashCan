import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import BetaNotification from '../../Components/BetaNotification';

const StatsAndReports = () => {
  return (
    <View style={{flex: 1, justifyContent: 'space-between'}}>
      <Text>StatsAndReports</Text>
      <BetaNotification />
    </View>
  );
};

export default StatsAndReports;

const styles = StyleSheet.create({});
