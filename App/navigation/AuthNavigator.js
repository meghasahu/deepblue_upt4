import {createStackNavigator} from 'react-navigation';
import Login from '../screens/signin/Login';
import Register from '../screens/signin/Register';

export default AuthStack = createStackNavigator({
    Login : Login,
});