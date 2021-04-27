import Axios from 'axios';
import React from 'react';
import {withRouter} from 'react-router-dom';
import App from './App';
import {useState} from "react";
import {useEffect} from "react";
import './Profile.css';

function Profile(props){
    //const [pickupCode, setPickupCode]=usestate(0);
    //const [depositCode, setDepositCode]=usestate(0);
    const email = props.location.email;
    const [password, setPassword]=useState('');
    const [name, setName]=useState('');
    const [pickupCode, setPickupCode]=useState(0);
    const [depositCode, setDepositCode]=useState(0);
    const [adminAccess, setAdminAccess]=useState(0);
    const [adminCode, setAdminCode]=useState(0);

    const reset = ()=>{
        setPickupCode(Math.floor(Math.random()*899999+100000));
        setDepositCode(Math.floor(Math.random()*899999+100000));
    }

    const resetAdmin = ()=>{
        setAdminCode(Math.floor(Math.random()*899999+100000));
    }

    React.useEffect(() => {
        setTimeout(()=>{
            Axios.post("http://localhost:3001/newCodes", {
            email:email, 
            depositCode:Math.floor(depositCode),
            pickupCode:Math.floor(pickupCode),
            adminCode:Math.floor(adminCode),
        });
           }, 1000)
    }, [pickupCode, depositCode, adminCode]);

    // React.useEffect(() => {
    //     Axios.post("http://localhost:3001/newAdminCode", {
    //         email:email, 
    //         adminCode:Math.floor(adminCode),
    //     });
    // }, [adminCode]);

    useEffect(() => {
        Axios.post("http://localhost:3001/getInfo",
        {email:email}).then((response)=>{
            //console.log(dict);
            setPassword(response.data[0].pwd);
            setName(response.data[0].customer_name);
            setPickupCode(response.data[0].pickup_code);
            setDepositCode(response.data[0].deposit_code);
            setAdminAccess(response.data[0].admin);
            setAdminCode(response.data[0].admin_password);
            //console.log(password);
            //console.log(depositCode);
            //console.log(depositCode);
        });
    }
        ,[]);
    if(adminAccess===0){
        return(
            <div className="ChangeCodes">
                <h1>Welcome {name}!</h1>
                <h1>Current Pickup and Deposit Codes</h1>
                    <div className="Label One">
                    <label>Pickup Code: {pickupCode}</label>
                    </div>
                    <div className="Label Two">
                    <label>Deposit Code: {depositCode}</label>
                    </div>
                    <div className="Button">
                    <button onClick={reset}>Get new pickup and deposit codes</button>
                    </div>
                {/* <div className="Admin">
                    <div>
                    <h1>{adminAccess ? 'Current Admin Password' : ''}</h1>
                    <label>{adminAccess ? 'Current Admin Password' : ''}</label>
                    <label>{adminAccess ? {adminCode} : ''}</label>
                    </div>
                </div> */}
            </div>
        );
    }
    else{
        return(
            <div className="ChangeCodes">
                <h1>Welcome {name}!</h1>
                <h1>Current Pickup and Deposit Codes</h1>
                    <div className="Label One">
                    <label>Pickup Code: {pickupCode}</label>
                    </div>
                    <div className="Label Two">
                    <label>Deposit Code: {depositCode}</label>
                    </div>
                    <div className="Button">
                    <button onClick={reset}>Get new pickup and deposit codes</button>
                    </div>
                     <div className="Admin">
                    <h1>Admin Information</h1>
                    <div>
                    <label> Current Admin Password: {adminCode}</label>
                    </div>
                    <button onClick={resetAdmin}>Get New Admin Password</button>
                </div> 
            </div>
        );
    }
}

export default withRouter(Profile)