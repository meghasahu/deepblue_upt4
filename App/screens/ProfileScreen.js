import React from 'react';
import {onSignOut} from '../components/Auth';
import {Container,Text,Button} from 'native-base';

export default class ProfileScreen extends React.Component {
  static navigationOptions = {
    title: 'Profile',
  };

  render() {
    /* Go ahead and delete ExpoConfigView and replace it with your
     * content, we just wanted to give you a quick view of your config */
    return (
      <Container>
    <Button onPress={()=>onSignOut(this.props.navigation)}><Text>SignOut</Text></Button>
    </Container>
    );
  }
}

