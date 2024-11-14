import {SafeAreaView, StatusBar, StyleSheet, Text, View} from 'react-native';
import React, {useContext} from 'react';
import {NavigationContainer} from '@react-navigation/native';
import RootNavigator from './src/Navigators/RootNavigator';
import userContext from './src/Context/userContext';

const App = () => {
  const [user, setUser] = React.useState(false);

  return (
    <NavigationContainer>
      <SafeAreaView style={{flex: 1}}>
        <userContext.Provider value={{user, setUser}}>
          <RootNavigator />
          {/* <Text>TrashCan</Text> */}
        </userContext.Provider>
      </SafeAreaView>
    </NavigationContainer>
  );
};

export default App;

const styles = StyleSheet.create({});
