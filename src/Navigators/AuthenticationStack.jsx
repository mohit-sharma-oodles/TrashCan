import {createStackNavigator} from '@react-navigation/stack';
import {SignIn, SplashScreen} from '../Screens/Authentication';

const Stack = createStackNavigator();

function AuthenticationStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}>
      <Stack.Screen name="Splash" component={SplashScreen} />
      <Stack.Screen name="SignIn" component={SignIn} />
      {/* <Stack.Screen name="SignUp" component={SignUp} /> */}
    </Stack.Navigator>
  );
}

export default AuthenticationStack;
