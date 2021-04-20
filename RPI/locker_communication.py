# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 17:27:48 2021

@author: joshn
"""

import serial
from time import sleep
import mysql.connector

mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )

mycursor=mydb.cursor()
lockers=[]


setup_mode=True

class locker:
    address=b'\x00\x00\x1b\x00\xbf'
    occupied=True
    username=''
    def __init__(self, address, occupied):
        self.address=address
        self.occupied=occupied



def setup():
    #ser = serial.Serial(port, baudrate, parity=serial.PARTITY_EVEN)
    global lockers
    port='/dev/ttyAMA0'
    baudrate=115200
    ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, timeout=1)
    #ser.open()
    global setup_mode
    addresses=set()
    while(setup_mode==True):
        #print(setup_mode)
        received_data=ser.read()
        sleep(0.03)
        data_left=ser.inWaiting()
        received_data += ser.read(data_left)
        if(len(received_data)>3):
            addresses.add(received_data)
            print(received_data)
    lockers=[]
    for address in addresses:
        lockers.append(locker(address, False))
    print(len(lockers))
    ser.close()
    for i in range(len(lockers)):
        print("Locker address: ", lockers[i].address)
    return lockers

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
    

def assign_locker(deposit_code):
    status,username=find_user_deposit(deposit_code)
    print("status "+str(status))
    print("Length of Lockers: "+str(len(lockers)))
    if(status==True):
        for i in range(len(lockers)):
            print("loop runs")
            if(lockers[i].occupied==False):
                print("If statement runs")
                lockers[i].occupied=True
                lockers[i].username=username
                open_locker(lockers[i].address)
                break
        
            
def unassign_locker(pickup_code):
    status,username=find_user_pickup(pickup_code)
    if(status==True):
        for i in range(len(lockers)):
            if(lockers[i].username==username):
                lockers[i].occupied=False
                lockers[i].username=''
                open_locker(lockers[i].address)
                print("Username" + lockers[i].username)
                break


def stop_setup():
    global setup_mode
    print("This runs")
    setup_mode=False

def open_locker(address):
    print("Open Locker Runs")
    #ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE)
    #input=bytearray(address)
    #print(input)
    #ser.write(b'\x9c\x9c\x1f\xc7\xbf\x78')
    port='/dev/ttyAMA0'
    baudrate=115200
    ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, timeout=1)
    #ser.open()
    print("Line before write")
    print(address)
    ser.write(address)
    print("Line after write")
    ser.close()

def read():
    #ser = serial.Serial ("/dev/ttyS0", 115200, parity=serial.PARITY_EVEN)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)         

#open_locker(b'432432423')
#read()



    
