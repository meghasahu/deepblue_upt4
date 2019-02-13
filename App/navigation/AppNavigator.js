import {createAppContainer,createSwitchNavigator } from 'react-navigation';

import MainTabNavigator from './MainTabNavigator';
import AuthNavigator from './AuthNavigator';
import AuthLoadingScreen from '../screens/AuthLoadingScreen';

export const AppNavigator = ()=>{
 return createAppContainer(createSwitchNavigator(
  {
  // You could add another route here for authentication.
  // Read more at https://reactnavigation.org/docs/en/auth-flow.html
  Loading : {
    screen : AuthLoadingScreen
  },
  Main: {
    screen : MainTabNavigator
  },
  Auth : {
    screen : AuthNavigator
  },
  },
  {
    initalRouteName : "Loading"   
  }
))};

