import React from 'react';
import { Form, Item, Label, Input,Button,Icon } from 'native-base';
import {View,StyleSheet,Text,AsyncStorage} from 'react-native';
import config from '../../fireconfig';
import firebase from 'firebase';
import {onSignIn} from '../../components/Auth';

// import { MonoText } from '../../components/StyledText';
//var userref = firebase.database().ref('users');

export default class Login extends React.Component {
  static navigationOptions = {
    title : 'SignIn',
  };

  state = {
    phoneNumber : null,
    code : null
  }

  componentDidMount(){
    if (!firebase.apps.length) {
      firebase.initializeApp(config);
  }
  }



  fetchData = (navigation) => {
    //var userRef = firebase.database().ref('users');
    // userRef.orderByChild("Phone number").equalTo(this.state.phone).once('value', (data) => {
    //   console.log(data.toJSON());
    // });
    const firebaseDb = firebase.database().ref('users/');
    const code = Number(this.state.code);
    const phone = Number(this.state.phoneNumber);
    firebaseDb.orderByChild('Code').equalTo(code).once('value', function (snapshot) {
      snapshot.forEach(function(childSnapshot) {
        var key = childSnapshot.key;
        snapshot.child(key).forEach(function(childSnap){
          if(childSnap.key=="Phone number"){
            if(childSnap.val()==phone){
              try {
                console.log("match");
               // _storeData(code,key);
                onSignIn(key);
                navigation.navigate('Main',{
                  code : key
                });
              } catch (error) {
                // Error saving data
              }
              
            }
          }          
        })     
    });
  });
}


  render() {
    return (
      <View style = {styles.container}>
        <Form>
          <Label>Phone Number</Label>
          <Item rounded style={styles.item}>
            <Input
            style={styles.input}
            keyboardAppearance="default"
            keyboardType="number-pad" 
            maxLength={10}
            onChangeText={value => this.setState({ phoneNumber: value })}
            value = {this.state.phoneNumber}/>
          </Item>
          <Label>Code</Label>

          <Item rounded style={styles.item}> 
            <Input
            secureTextEntry={true}
            keyboardAppearance="default"
            keyboardType="number-pad" 
            maxLength={4}
            onChangeText={value => this.setState({ code: value })}
            value = {this.state.code}
            style={styles.input}/>
          </Item>
          <Button
          iconLeft primary large
          style={styles.button}
          onPress={()=>this.fetchData(this.props.navigation)}>
            <Icon name='login' type='Entypo'/>
            <Text style={styles.buttonText}>Login</Text>
          </Button>
        </Form>
      </View>
    );
  }

}

const styles = StyleSheet.create({
container : {
  flex : 1,
  flexDirection : 'column',
  justifyContent : 'center',
  alignItems : 'center',
  alignContent : 'center',
  marginHorizontal: 10,
  paddingHorizontal : 20
},
item :{
  padding : '1%',
  marginBottom : '2%'
},
label:{
  marginTop : '5%'
},
input:{
  padding : '3%',
},
button : {
  width : '60%',
  height : '18%',
  margin : '3%'
},
buttonText:{
  color : 'white',
  fontSize : 20
}
})