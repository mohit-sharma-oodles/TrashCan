import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import BetaNotification from '../../Components/BetaNotification';

const ReturnOfTrash = () => {
  return (
    <View>
      <Text style={{flex: 1, justifyContent: 'space-between'}}>
        ReturnOfTrash
      </Text>
      <BetaNotification />
    </View>
  );
};

export default ReturnOfTrash;

const styles = StyleSheet.create({});
