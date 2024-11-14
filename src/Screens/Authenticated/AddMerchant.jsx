import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import BetaNotification from '../../Components/BetaNotification';

const AddMerchant = () => {
  return (
    <View style={{flex: 1, justifyContent: 'space-between'}}>
      <Text>AddMerchant</Text>
      <BetaNotification />
    </View>
  );
};

export default AddMerchant;

const styles = StyleSheet.create({});
