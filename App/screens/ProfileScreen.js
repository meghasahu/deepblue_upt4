import React from 'react';
import {onSignOut} from '../components/Auth';
import { Container, Content, Header, Left, Body, Right, Button, Title, ListItem, Text,Card, CardItem, Thumbnail, Icon} from 'native-base';
import {AsyncStorage,RefreshControl,ScrollView} from 'react-native';
import * as Progress from 'react-native-progress';
import config from '../fireconfig';
import firebase from 'firebase';

export default class ProfileScreen extends React.Component {
  static navigationOptions = {
    title: 'Profile',
  };

  constructor(props) {
    super(props);
    this.state = {
     // scrollY: new Animated.Value(0),
      activeIndex:0,
      streak : 0,
      incentives : 0,
      key : null,
      isFetched : false,
      phone : null,
      code : null,
      refreshing : false
    };
  }

  refreshData=async(key)=>{
    firebase.database().ref('user_streak/'+key).once('value',snapshot=>{
      const streak = snapshot.val().streak;
      const incentives = snapshot.val().total_incentives;
      this.setState({streak : streak, incentives : incentives });
    });
  }

  fetchData = async(key) =>{
    firebase.database().ref('user_streak/'+key).once('value',snapshot=>{
      const streak = snapshot.val().streak;
      const incentives = snapshot.val().total_incentives;
      this.setState({streak : streak, incentives : incentives });
    });
    firebase.database().ref('users/'+key).once('value',snapshot=>{
      const phone = snapshot.val()['Phone number'];
      const code = snapshot.val().Code;
      this.setState({phone : phone, code : code});
    })
  }

  componentWillMount = async() =>{
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
    /* Go ahead and delete ExpoConfigView and replace it with your
     * content, we just wanted to give you a quick view of your config */
    return (
      <ScrollView
      refreshControl = {<RefreshControl
            refreshing={this.state.refreshing}
            onRefresh={this._onRefresh}
          />
        }>
        <Container>
      <Content>
      <Card>
            <CardItem>
              <Left>
                <Thumbnail source={{uri: 'https://png.pngtree.com/svg/20160307/user_outline_72990.png'}} />
                <Body>
                  <Text style={{alignContent:'flex-start'}}>{this.state.key}</Text>
                </Body>
              </Left>
            </CardItem>
            <CardItem cardBody>
              <Left style={{flexDirection: 'column', marginHorizontal : '5%', padding : '1%',alignContent:'center', justifyContent : 'center'}}>
                <Progress.Circle progress={100} size={120} showsText={true} formatText={()=>{ return this.state.streak}}/>
                <Text>Streak</Text>
              </Left>
              <Right style={{flexDirection: 'column', marginHorizontal : '5%', padding : '1%',alignContent:'center', justifyContent : 'center'}}>
                <Progress.Circle progress={100} size={120} showsText={true} formatText={()=>{ return this.state.incentives}}/>
                <Text>Total Incentives</Text>
              </Right>
            </CardItem>
            <CardItem>
              <Left>
                <Text>Congratulations! </Text>
                <Text note>{this.state.streak} days of continuous use!</Text>
              </Left>
            </CardItem>
          </Card>
          <Card>
          <CardItem>
              <Icon type="Entypo" active name="phone" />
              <Text>Phone number : {this.state.phone}</Text>
            </CardItem>
            <CardItem onPress={this.state.codeInput}>
              <Icon type="Entypo" active name="code" />
              <Text>Your Code : {this.state.code}</Text>
            </CardItem>
            <CardItem style={{justifyContent:'center'}}>
              <Button onPress={()=>onSignOut(this.props.navigation)}>
              <Text>Logout</Text>
              </Button>
            </CardItem>
           </Card>

      </Content>
    </Container>
      </ScrollView>
      
    );
  }
}

