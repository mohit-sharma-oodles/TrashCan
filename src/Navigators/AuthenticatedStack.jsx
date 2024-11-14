import {
  HomeScreen,
  AddMerchant,
  Departure,
  ReturnOfTrash,
  Stats,
} from '../Screens/Authenticated';

import {useContext} from 'react';
import userContext from '../Context/userContext';

import {
  DrawerContentScrollView,
  DrawerItem,
  DrawerItemList,
  createDrawerNavigator,
} from '@react-navigation/drawer';
import {useTranslation} from 'react-i18next';
import {View} from 'react-native';

const Drawer = createDrawerNavigator();

function CustomDrawerContent(props) {
  const {setUser} = useContext(userContext);
  const {t} = useTranslation();

  return (
    <View style={{flex: 1}}>
      <DrawerContentScrollView {...props}>
        <DrawerItemList {...props} />
      </DrawerContentScrollView>
      <DrawerItem label={t('Disconnect')} onPress={() => setUser(false)} />
    </View>
  );
}

function AuthenticatedStack() {
  const {t} = useTranslation();
  const {user, setUser} = useContext(userContext);
  return (
    <Drawer.Navigator
      screenOptions={{
        headerTitleAlign: 'center',
      }}
      drawerContent={props => <CustomDrawerContent {...props} />}>
      <Drawer.Screen name={t('Welcome')} component={HomeScreen} />
      <Drawer.Screen name={t('Add a merchant')} component={AddMerchant} />
      <Drawer.Screen
        name={t('Departure from a trash can')}
        component={Departure}
      />
      <Drawer.Screen
        name={t('Return of a trash can')}
        component={ReturnOfTrash}
      />
      <Drawer.Screen name={t('Statistic')} component={Stats} />
      {/* <DrawerItem label="Logout" onPress={() => setUser(false)} /> */}
    </Drawer.Navigator>
  );
}

export default AuthenticatedStack;
