const express = require("express");
const mysql = require("mysql");
const cors = require("cors");

const app= express();

app.use(express.json());
app.use(cors());
const db =mysql.createConnection({
    user: "ece445",
    host: "98.212.157.222",
    password: "ECE 445 Team 61",
    database:"locker"
  });

  app.post('/login', (req, res)=>{

    const email= req.body.email;
    const password= req.body.password;

    db.query("SELECT email, pwd FROM locker WHERE email=? and pwd=?",
    [email,password],
    (err,result)=>{
        //console.log(email);
        //console.log(password);
        if(err){
            res.send({err:err});
        }
        else{
            if(result.length>0){
                //console.log(result);
                res.send(result);
            }
            else{
                //console.log("Not found");
                res.send({message: "Wrong email or password"});
            }
        }
    });
});

app.post('/newCodes', (req, res)=>{

    const email= req.body.email;
    const pickupCode= req.body.pickupCode;
    const depositCode= req.body.depositCode;
    const adminCode=req.body.adminCode;

    db.query("UPDATE locker SET pickup_code=?, deposit_code=?, admin_password=? WHERE email=?",
    [pickupCode, depositCode, adminCode, email],
    (err,result)=>{
        console.log(pickupCode);
        console.log(depositCode)
        console.log(result);
        //console.log(email);
        //console.log(password);
        if(err){
            res.send({err:err});
        }
       
    });
});

app.post('/newAdminCode', (req, res)=>{

    const email= req.body.email;
    const adminCode= req.body.adminCode;
    
    db.query("UPDATE locker SET admin_password=? WHERE email=?",
    [adminCode, email],
    (err,result)=>{
        //console.log(email);
        //console.log(password);
        if(err){
            res.send({err:err});
        }
       
    });
});

app.post('/getInfo', (req, res)=>{

    const email= req.body.email;

    db.query("SELECT email, pwd, customer_name, pickup_code, deposit_code, admin, admin_password FROM locker WHERE email=?",
    [email],
    (err,result)=>{
        //console.log(email);
        //console.log(password);
        if(err){
            res.send({err:err});
        }
        else{
           res.send(result);
        }
    });
});


// app.post('/newcode', (req, res)=>{

//     const pickupCode= req.body.pickupCode;
//     const depositCode= req.body.dropoffCode;

//     db.query("SELECT pickup_code, deposit_code FROM locker WHERE pickup_code=? OR deposit_code=?",
//     [pickupCode,depositCode],
//     (err,result)=>{
//         if(err){
//             res.send({err:err});
//         }
//         else{
//             if(result.length==0){
//                 res.send(result);
//             }
//             else{
//                 console.log("Matching Code Exists");
//                 res.send({message: "New Code is required"});
//             }
//         }
//     });
// });

app.post('/register', (req, res)=>{

    const email= req.body.email;
    const password= req.body.password;
    const customerName= req.body.customerName;
    const pickupCode=req.body.pickupCode;
    const depositCode=req.body.dropoffCode;

    db.query("INSERT INTO locker (email, pwd, customer_name, pickup_code, deposit_code, admin, admin_password) VALUES (?,?,?,?,?,?,?)", 
    [email, password,customerName, pickupCode, depositCode, 0, 0],
    (err,result)=>{
        console.log(err);
    });
});

app.listen(3001, ()=>{
    console.log("running server");
});