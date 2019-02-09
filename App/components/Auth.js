import { AsyncStorage } from "react-native";

export const onSignIn = () => {
    AsyncStorage.setItem("code", "true");
};

export const onSignOut = (navigation) => {
    AsyncStorage.removeItem("code").then(()=>navigation.navigate('Auth'))
    
}
