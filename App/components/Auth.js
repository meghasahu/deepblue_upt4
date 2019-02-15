import { AsyncStorage } from "react-native";

export const onSignIn = (key) => {
    AsyncStorage.setItem("code", "true");
    AsyncStorage.setItem("key", key);
};

export const onSignOut = (navigation) => {
    AsyncStorage.removeItem("code").then(()=>navigation.navigate('Auth'))
    
}
