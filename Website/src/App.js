import {useState} from "react";
import './App.css';
import {BrowserRouter as Router, Link, Route, Switch } from "react-router-dom";
import ProtectedRoute from './ProtectedRoute.js';
import Profile from './Profile.js';
import Axios from 'axios';




function App() {
  const [isAuth, setIsAuth]= useState(false);
  const [emailReg, setEmailReg]= useState('');
  const [passwordReg, setPasswordReg]= useState('');
  const [customerName, setCustomerName]=useState('');
  const [email, setEmail]=useState('');
  const [password, setPassword]=useState('');
  const [wrongInfo, setWrongInfo]=useState('');
  const [pickupCodeReg, setPickupCodeReg]= useState(0);
  const [dropoffCodeReg, setDropoffCodeReg]= useState(0);
  const [registrationStatus, setRegistrationStatus]=useState(0);
  

  // const randomCode = ()=>{
  //   setPickupCodeReg(Math.random()*89999+10000);
  //   setDropoffCodeReg(Math.random()*89999+10000);
  //   Axios.post("http://localhost:3001/newcode",{
  //     pickupCode:pickupCodeReg,
  //     dropoffCode:dropoffCodeReg}).then((response)=>{
  //       if(response.data.message){
  //         randomCode;
  //       }
  //     });
  // };


  const register = ()=>{
    setPickupCodeReg(Math.floor(Math.random()*899999+100000))
    setDropoffCodeReg(Math.floor(Math.random()*899999+100000))
    setRegistrationStatus(1)
    Axios.post("http://localhost:3001/register", {
      email: emailReg,
      password: passwordReg,
      customerName: customerName,
      pickupCode: pickupCodeReg,
      dropoffCode: dropoffCodeReg}).then((response)=>{
        if(response.data.err){
          setPickupCodeReg(Math.floor(Math.random()*899999+100000))
          setDropoffCodeReg(Math.floor(Math.random()*899999+100000))
          Axios.post("http://localhost:3001/register", {
          email: emailReg,
          password: passwordReg,
         customerName: customerName,
          pickupCode: pickupCodeReg,
          dropoffCode: dropoffCodeReg})
        }
      })
  };
  
  const login = ()=>{
    Axios.post("http://localhost:3001/login", {
      email: email,
      password: password}).then((response)=>{
        //console.log(response.data)
        if(response.data.message){
          setIsAuth(false);
          setWrongInfo("Email or Password is Incorrect");
        }
        else{
          setIsAuth(true);
          setWrongInfo("Information is Correct, Welcome");
        }
      });
  };
  
  return( <Router>
    <Route path ="/" exact>

      <div className="App">
        <h1>EML</h1> 
        <div className="registration">
          <h1>Registration</h1>
          <label>Your Name</label>
          <input type="text"onChange={(e)=>{
            setCustomerName(e.target.value);
          }}/>
          <label>Email</label>
          <input type="text" onChange={(e)=>{
            setEmailReg(e.target.value);
          }}/>
          <label>Password</label>
          <input type="text" onChange={(e)=>{
            setPasswordReg(e.target.value);
          }}/>
          <button onClick={register}>Register</button>
          <div>
          <label>{registrationStatus? 'You have successfully registered': ''}</label>
          </div>
        </div>
        <div className="login">
          <h1>Login</h1>
          <input type="text" placeholder="Email..." onChange={(e)=>{
            setEmail(e.target.value);
          }}/>
          <input type="text" placeholder="Password..." onChange={(e)=>{
            setPassword(e.target.value);
          }}/>
          <button 
            onClick={()=>{
            setIsAuth(true);
            login();
            //console.log(email);
           }}>Login</button>
        </div>
        <h1>{wrongInfo}</h1>
      </div>
      <div className="Link">
        <Link to={{pathname:"/profile",
        email}}
        >Go to Profile

        </Link>
        </div>
    </Route>
    <ProtectedRoute path="/profile" component={Profile} isAuth={isAuth}/>
  </Router>
  );
}

export default App;
