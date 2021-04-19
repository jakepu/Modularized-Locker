# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 16:05:24 2021

@author: joshn
"""
import mysql.connector
from locker_communication import open_locker

mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )

mycursor=mydb.cursor()

class locker:
    address=1000
    occupied=True
    username=''
    def __init__(self, address, occupied):
        self.addresss=address
        self.occupied=occupied

def find_user_deposit(deposit_code):
    value=(deposit_code,)
    mycursor.execute("SELECT username FROM locker WHERE deposit_code= %s", value)
    result=mycursor.fetchall()
    print(result)
    found=False
    username=''
    if(len(result)!=0):
        found=True
        username=result[0][0]
    return(found, username)

def find_user_pickup(pickup_code):
    value=(pickup_code,)
    mycursor.execute("SELECT username FROM locker WHERE pickup_code= %s", value)
    result=mycursor.fetchall()
    found=False
    username=''
    if(len(result)!=0):
        found=True
        username=result[0][0]
    return(found, username)
    

def assign_locker(deposit_code, lockers):
    status,username=find_user_deposit(deposit_code)
    if(status==True):
        for i in range(len(lockers)):
            if(lockers[i].occupied==False):
                lockers[i].occupied=True
                lockers[i].username=username
                open_locker(lockers[i].address)
                break
        
            
def unassign_locker(pickup_code, lockers):
    status,username=find_user_pickup(pickup_code)
    if(status==True):
        for i in range(len(lockers)):
            if(lockers[i].username==username):
                lockers[i].occupied=False
                lockers[i].username=''
                open_locker(lockers[i].address)
                print("Username" + lockers[i].username)
                break


                

