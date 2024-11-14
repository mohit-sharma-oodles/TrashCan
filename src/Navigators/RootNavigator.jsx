import React, {useContext} from 'react';
import AuthenticationStack from './AuthenticationStack';
import AuthenticatedStack from './AuthenticatedStack';
import userContext from '../Context/userContext';

export default function RootNavigator() {
  const {user} = useContext(userContext);
  return (
    <>{user === true ? <AuthenticatedStack /> : <AuthenticationStack />}</>
  );
}
