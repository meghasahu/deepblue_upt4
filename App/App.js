import React from 'react';
import { Platform, StatusBar, StyleSheet, View } from 'react-native';
import {AppNavigator} from './navigation/AppNavigator';
import { AppLoading, Font} from 'expo';

export default class App extends React.Component {
  
  state={
    fontsAreLoaded : false
  }
  
  
  async componentWillMount() {
    await Font.loadAsync({
        'Roboto': require('./node_modules/native-base/Fonts/Roboto.ttf'),
        'Roboto_medium': require('./node_modules/native-base/Fonts/Roboto_medium.ttf'),
      });
    this.setState({fontsAreLoaded: true});
}

  render() {
    const fonts = this.state.fontsAreLoaded;
    const Layout = AppNavigator();
    if(fonts){
      return (
        <View style={styles.container}>
          {Platform.OS === 'android' && <View style={{
          height : '4%',
          backgroundColor : 'black',
        }} />}
          {Platform.OS === 'ios' && <StatusBar barStyle="default" />}
          <Layout/>
        </View>
      );
    }
    else{
      return <AppLoading
      onError={console.warn}
      />
    }
  }
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
