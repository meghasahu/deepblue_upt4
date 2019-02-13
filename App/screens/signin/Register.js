import React, { Component } from 'react';
import { Container, Header, Content, Form, Item, Input, Label, Button } from 'native-base';
import config from '../../fireconfig';
import firebase from 'firebase';
import { Text, View } from 'react-native';

export default class Register extends Component {
  
  state={
    Name:'',
    Email:'',
    Phone:''
  }

  static navigationOptions = {
    title : "Profile Update"
  }

  componentDidMount(){
    if (!firebase.apps.length) {
      firebase.initializeApp(config);
    }
  }
  handleChange = (e) => {
    this.setState({
        [e.target.name]: e.target.value
    })
  }

  onSubmit = (e,navigation) => {
    
    navigation.navigate('Main');
  }
  
  render(){
    return (
      <Container>
        <Content>
          <Form>
            <Item floatingLabel>
              <Label>Name</Label>
              <Input name='Name' value={this.state.Name} onChange={e => this.handleChange(e)}/>
            </Item>
            <Item floatingLabel>
              <Label>Phone number</Label>
              <Input name='Phone' value={this.state.Phone} onChange={e => this.handleChange(e)}/>
            </Item>
            <Item floatingLabel>
              <Label>Email id</Label>
              <Input name='Email' value={this.state.Email} onChange={e => this.handleChange(e)}/>
            </Item>
            <Item floatingLabel last>
              <Label>Password</Label>
              <Input name='Password' value={this.state.Password} onChange={e => this.handleChange(e)}/>
            </Item>
            <Button onPress={() => this.onSubmit(this.props.navigation)}><Text> Register </Text></Button>
          </Form>
        </Content>
      </Container>
    );
  }
}