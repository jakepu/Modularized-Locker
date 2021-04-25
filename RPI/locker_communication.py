# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 17:27:48 2021

@author: joshn
"""

import serial
from time import sleep
import mysql.connector
import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO

# setup RE / WE pin on RPI
RS485_EN_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(RS485_EN_PIN, GPIO.OUT)
GPIO.output(RS485_EN_PIN, GPIO.LOW)                 # default RE on, DE off

lockers=[]

setup_mode=True

class locker:
    address=b'\x00\x00\x1b\x00\xbf'
    occupied=True
    email=''
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

def dropoff_email(email):
    try:
        msg = EmailMessage()
        msg.set_content('A package has arrived for you.')

        msg['Subject'] = 'New Package'
        msg['From'] = "ece445lockertest@gmail.com"
        msg['To'] = email

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("ece445lockertest@gmail.com", "Illini@01")
        server.send_message(msg)
        server.quit()
    except:
        print("Not a valid email")

def pickup_email(email):
    try:
        msg = EmailMessage()
        msg.set_content('A package at your locker has just been picked up.')

        msg['Subject'] = 'New Package'
        msg['From'] = "ece445lockertest@gmail.com"
        msg['To'] = email

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("ece445lockertest@gmail.com", "Illini@01")
        server.send_message(msg)
        server.quit()
    except:
        print("Not a valid email")

    
    
def find_user_deposit(deposit_code):
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    value=(deposit_code,)
    mycursor.execute("SELECT email FROM locker WHERE deposit_code= %s", value)
    result=mycursor.fetchall()
    print(result)
    found=False
    mydb.close()
    email=''
    if(len(result)!=0):
        found=True
        email=result[0][0]
    if(len(deposit_code)<4):
        found=False
    return(found, email)

def find_user_pickup(pickup_code):
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    value=(pickup_code,)
    mycursor.execute("SELECT email FROM locker WHERE pickup_code= %s", value)
    result=mycursor.fetchall()
    found=False
    mydb.close()
    email=''
    if(len(result)!=0):
        found=True
        email=result[0][0]
    return(found, email)
    

def assign_locker(deposit_code):
    status,email=find_user_deposit(deposit_code)
    print("status "+str(status))
    print("Length of Lockers: "+str(len(lockers)))
    if(status==True):
        for i in range(len(lockers)):
            print("loop runs")
            if(lockers[i].occupied==False):
                print("If statement runs")
                lockers[i].occupied=True
                lockers[i].email=email
                open_locker(lockers[i].address)
                dropoff_email(email)
                break
        
    return status
        
            
def unassign_locker(pickup_code):
    status,email=find_user_pickup(pickup_code)
    if(status==True):
        for i in range(len(lockers)):
            if(lockers[i].email==email):
                lockers[i].occupied=False
                lockers[i].email=''
                open_locker(lockers[i].address)
                print("email" + lockers[i].email)
                pickup_email(email)
                break
    return status

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
    GPIO.output(RS485_EN_PIN, GPIO.HIGH)            # Turn on DE, turn off RE
    ser.write(address)
    GPIO.output(RS485_EN_PIN, GPIO.LOW)             # Turn on RE, turn off DE
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

dropoff_email('email')
#open_locker(b'432432423')
#read()



    
