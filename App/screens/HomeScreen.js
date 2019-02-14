import React from 'react';
import { Container, Header, Content, Card, CardItem, Body,Right, Button,View } from 'native-base';
import {Text,StyleSheet,AsyncStorage,ScrollView,RefreshControl} from 'react-native';
import {AppLoading} from 'expo';
import * as Progress from 'react-native-progress';
import config from '../fireconfig';
import firebase from 'firebase';

// import { MonoText } from '../../components/StyledText';

export default class HomeScreen extends React.Component {
  static navigationOptions = {
    title : 'Home',
  };

  constructor(props){
    super(props);
    this.state={
      isFetched : false,
      key : null,
      streak : 0,
      total_incentives : 0,
      percentage : 0,
      completedStreak : 0,
      activeStreak : 0,
      disableButton : true,
      refreshing : false,
      time_in : null,
      time_out : null
    };
  }


  checkPercentage = () => {
    const streak = this.state.streak;
    const activeStreak = this.state.activeStreak;
    const div = (streak/activeStreak);
    const percentage = div*100;
    const convPerc = Math.floor(percentage);
    this.setState({percentage : convPerc})
  }

  checkActiveStreak = () =>{
    const compStreak = this.state.completedStreak;
    if(compStreak == 0) {
      this.setState({activeStreak : 1});
    }
    else if(compStreak==1){
      this.setState({activeStreak : 2});
    }
    else if(compStreak==2){
      this.setState({activeStreak : 5})
    }
    else if(compStreak==5){
      this.setState({activeStreak : 10})
    }
    else if(compStreak==10){
      this.setState({activeStreak : 20})
    }
    else if(compStreak==20){
      this.setState({activeStreak : 30})
    }
    else if(compStreak==30){
      this.setState({activeStreak : 60})
    }

  }

  trimString = (time_in,time_out) => {
    let string1 = time_in;
    let string2 = time_out;
    let newString1 = string1.substring(0,19);
    let newString2 = string2.substring(0,19);
    this.setState({time_in : newString1, time_out : newString2})
  }

  refreshData = async(key) => {
    firebase.database().ref('user_streak/'+key).once('value',snapshot=>{
      const streak = snapshot.val().streak;
      const incentives = snapshot.val().total_incentives;
      const compStreak = snapshot.val().completedStreak;
      this.setState({streak : streak, total_incentives : incentives, completedStreak : compStreak });
      this.checkActiveStreak();
      this.checkPercentage();
      const percentage = this.state.percentage;
      const disable = percentage==100 ? false : true;
      this.setState({disableButton : disable });
    });
    firebase.database().ref('usage/').orderByChild('key').equalTo(key).limitToLast(1).once('value',snapshot=>{
      let childkey = null;
      snapshot.forEach(function(childsnapshot){
        childkey = childsnapshot.key;
      });
      const time_in = snapshot.child(childkey).val()['time_in'];
      const time_out = snapshot.child(childkey).val()['time_out'];
      this.trimString(time_in,time_out);
      
    });
  }


  fetchData = async(key) =>{
    firebase.database().ref('user_streak/'+key).once('value',snapshot=>{
      const streak = snapshot.val().streak;
      const incentives = snapshot.val().total_incentives;
      const compStreak = snapshot.val().completedStreak;
      this.setState({streak : streak, total_incentives : incentives, completedStreak : compStreak });
      this.checkActiveStreak();
      this.checkPercentage();
      const percentage = this.state.percentage;
      const disable = percentage==100 ? false : true;
      this.setState({disableButton : disable});
    });

    firebase.database().ref('usage/').orderByChild('key').equalTo(key).limitToLast(1).once('value',snapshot=>{
      let childkey = null;
      snapshot.forEach(function(childsnapshot){
        childkey = childsnapshot.key;
      });
      const time_in = snapshot.child(childkey).val()['time_in'];
      const time_out = snapshot.child(childkey).val()['time_out'];
      this.trimString(time_in,time_out);     
    });
    
  }

  redeem = (key) => {
    let active = this.state.activeStreak;
    let tot = 0
    console.log("active ",active);
    if(active==1){
      tot = 5;
    }
    else if(active==2){
      tot = 10;
    }
    else if(active==5){
      tot = 20;
      console.log(tot);
    }
    else if(active==10){
      tot = 50;
    }
    else if(active==20){
      tot = 100;
    }
    else if(active==30){
      tot = 500;
    }
    else if(active==60){
      tot = 1000;
    }
    this.setState(previousState => ({total_incentives : tot + previousState.total_incentives}),()=>
    {firebase.database().ref('user_streak/'+key).update({
        completedStreak : active,
        total_incentives : this.state.total_incentives
      })})
    this.refreshData(key);
  }

  componentDidMount = async() =>{
    if (!firebase.apps.length) {
      firebase.initializeApp(config);
  }
    var key1 = await AsyncStorage.getItem("key");
    this.setState({key : key1})
    if(!this.state.isFetched){
      this.fetchData(this.state.key);
    }
    
  }

  _onRefresh = () => {
    this.setState({refreshing: true});
    this.refreshData(this.state.key).then(() => {
      this.setState({refreshing: false});
    });
  }

  

  render() {
    const percentage = this.state.percentage;
      return (
        <ScrollView
        refreshControl={
          <RefreshControl
            refreshing={this.state.refreshing}
            onRefresh={this._onRefresh}
          />
        }>
          <Container>
          
          <Card>
          <CardItem header>
            <Text style={{color : 'blue', fontSize : 20 }}>Current Streak : {this.state.activeStreak} Day Streak</Text>
          </CardItem>
          <CardItem style={styles.streakCycle}>
            <Progress.Circle progress={percentage/100} size={150} showsText={true} formatText={()=>{ return percentage}}/>
          </CardItem>
            <CardItem style={styles.redeemButton}>
            <Button disabled={this.state.disableButton} onPress={()=>this.redeem(this.state.key)}>
                <Text>Redeem</Text>
            </Button>
            </CardItem>
          </Card>
          <Card>
            <CardItem header>
              <Text style={{color : 'blue', fontSize : 15 }}>
                Latest Usage :
              </Text>
            </CardItem>
            <CardItem>
              <Body>
                <Text style={{fontSize : 15 }}>Time In : {this.state.time_in}</Text>
                <Text style={{fontSize : 15 }}>Time Out : {this.state.time_out}</Text>
              </Body>
            </CardItem>
          </Card>      
        </Container>
        </ScrollView>
        //<View><Text>Hello</Text></View>
      );
  }

}

const styles = StyleSheet.create({
  streakCycle:{   
    flexDirection : 'column',
    justifyContent : 'center',
    alignitems : 'center',
    height: 175
  },
  redeemButton : {
    justifyContent : 'center',
    alignContent : 'center'
  }
});
