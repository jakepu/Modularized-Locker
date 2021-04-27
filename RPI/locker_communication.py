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
import time
import pickle
import ast

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
    unit_ID='0'
    number=76
    unit_ID='0'
    def __init__(self, address, occupied, number, unit_ID, email):
        self.address=address
        self.occupied=occupied
        self.number=number
        self.unit_ID=unit_ID
        self.email=email



def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

def bytes_to_str(b):
    ret = ''
    for each_byte in b:
        ret += str(int(each_byte)) + ':'
    ret = ret [:-1]
    return ret

def str_to_bytes(s):
    arr = s.split(':')
    ret = b''
    for each_int in arr:
        ret += int(each_int).to_bytes(1, byteorder = 'little')
    return ret

def restore():
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    sql='SELECT * from backup WHERE ID=%s'
    val=(getserial(),)
    mycursor.execute(sql, val)
    result=mycursor.fetchall()
    #print(result)
    for i in range(len(result)):
        occupied=False
        if(result[i][3]!='NULL'):
            occupied=True
        lockers.append(locker(str_to_bytes(result[i][2]), occupied, result[i][1], result[i][0], result[i][3]))

def string_to_hext(string):
    h=[]
    for i in range(len(string)):
        if(string[i]=='x'):
            hex.append(string[i+1]+string[i+2])
    h=[]
    for i in range(len(h)):
        h[i]=hex(int(h[i],16))


def setup():
    #ser = serial.Serial(port, baudrate, parity=serial.PARTITY_EVEN)
    global lockers
    port='/dev/ttyAMA0'
    baudrate=115200
    ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, timeout=1)
    #ser.open()
    global setup_mode
    setup_mode=True
    addresses=set()
    while(setup_mode==True):
        #print(setup_mode)
        received_data=ser.read()
        sleep(0.03)
        data_left=ser.inWaiting()
        received_data += ser.read(data_left)
        if(len(received_data)>3):
            addresses.add(received_data)
            #print(received_data)
    lockers=[]
    mySerial=getserial()
    for address in addresses:
        lockers.append(locker(address, False, len(lockers)+1, mySerial, ''))
    #print(len(lockers))
    ser.close()
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    #mycursor.get_warning = True
    value=(mySerial,)
    mycursor.execute("SELECT ID FROM backup WHERE ID= %s", value)
    result=mycursor.fetchall()
    if(len(result)>0):
        mycursor.execute("DELETE FROM backup WHERE ID= %s", value)
    sql="INSERT INTO backup (ID, Locker_Number, Address, occupied_email) VALUES(%s,%s,%s,%s) "
    for i in range(len(lockers)):
        val=(mySerial, lockers[i].number, bytes_to_str(lockers[i].address), "NULL")
        mycursor.execute(sql,val)
        #print("Number of rows affected: ", mycursor.rowcount)
    mydb.commit()
    mydb.close()
    return lockers

def dropoff_email(email, number):
    try:
        msg = EmailMessage()
        msg.set_content('A package has arrived for you in locker number '+str(number)+'.')

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
        msg.set_content('A package has just been picked up. If you did not recieve this package please contact your administrator.')

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

def open_all_lockers():
    for i in range(len(lockers)):
        open_locker(lockers[i].address)
        time.sleep(8)    

    
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
    #print(result)
    found=False
    #mydb.close()
    email=''
    if(len(result)!=0):
        found=True
        email=result[0][0]
    if(len(deposit_code)<4):
        found=False
    # value=(getserial(), )
    # mycursor.execute("UPDATE backup SET occupied_email =%s WHERE (ID, Locker_Number)=(%s,%s)", value)
    # result=mycursor.fetchall()
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
    #print("status "+str(status))
    #print("Length of Lockers: "+str(len(lockers)))
    number=0
    locker_assigned=False
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    if(status==True):
        for i in range(len(lockers)):
            #print("loop runs")
            
            if(lockers[i].occupied==False):
               # print("If statement runs")
                lockers[i].occupied=True
                lockers[i].email=email
                number=lockers[i].number
                open_locker(lockers[i].address)
                dropoff_email(email, lockers[i].number)
                sql='UPDATE backup SET occupied_email=%s WHERE ID=%s and Locker_Number=%s'
                vals=(email, lockers[i].unit_ID, lockers[i].number)
                #print(vals)
                mycursor.execute(sql, vals)
                #print("Locker Number: ", lockers[i].number)
                #print("Length of lockers: ", len(lockers))
                locker_assigned=True
                mydb.commit()
                mydb.close()
                break
        #print("Number sent to GUI: ", number)
    return status, number, locker_assigned
        
            
def unassign_locker(pickup_code):
    status,email=find_user_pickup(pickup_code)
    numbers=[]
    locker_unassigned=False
    mydb= mysql.connector.connect(
        host="98.212.157.222",
        user= "ece445",
        password= "ECE 445 Team 61",
        database= "locker",
        auth_plugin='mysql_native_password'
        )
    mycursor=mydb.cursor()
    if(status==True):
        for i in range(len(lockers)):
            if(lockers[i].email==email):
                lockers[i].occupied=False
                lockers[i].email=''
                numbers.append(lockers[i].number)
                open_locker(lockers[i].address)
               # print("email" + lockers[i].email)
                pickup_email(email)
                locker_unassigned=True
                sql='UPDATE backup SET occupied_email=%s WHERE ID=%s and Locker_Number=%s'
                vals=('NULL', lockers[i].unit_ID, lockers[i].number)
                mycursor.execute(sql, vals)
                time.sleep(8)
    mydb.commit()
    mydb.close()
    return status, numbers, locker_unassigned

def stop_setup():
    global setup_mode
    #print("This runs")
    setup_mode=False

def open_locker(address):
    #print("Open Locker Runs")
    #ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE)
    #input=bytearray(address)
    #print(input)
    #ser.write(b'\x9c\x9c\x1f\xc7\xbf\x78')
    port='/dev/ttyAMA0'
    baudrate=115200
    ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE, timeout=1)
    #ser.open()
    #print("Line before write")
    #print(address)
    GPIO.output(RS485_EN_PIN, GPIO.HIGH)            # Turn on DE, turn off RE
    ser.write(address)
    time.sleep(0.5)
    GPIO.output(RS485_EN_PIN, GPIO.LOW)             # Turn on RE, turn off DE
    #print("Line after write")
    ser.close()

def read():
    #ser = serial.Serial ("/dev/ttyS0", 115200, parity=serial.PARITY_EVEN)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        #print (received_data)         

#dropoff_email('email')
#open_locker(b'432432423')
#read()

    
