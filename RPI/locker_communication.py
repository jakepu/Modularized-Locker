# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 17:27:48 2021

@author: joshn
"""

import serial
from time import sleep

def setup(setup_mode):
    port='/dev/ttyS0'
    baudrate=115200
    
    #ser = serial.Serial(port, baudrate, parity=serial.PARTITY_EVEN)
    
    addresses=[]
    while(setup_mode==True):
        received_data=ser.read()
        sleep(0.03)
        data_left=ser.inWaiting()
        received_data += ser.read(data_left)
        addresses.append(received_data)
    lockers=[]
    for i in range(len(addresses)):
        lockers.append(locker(addresses[i], False))
    return lockers


def open_locker(address):
    print("Open Locker Runs")
    port='/dev/ttyAMA0'
    baudrate=115200
    ser = serial.Serial(port, baudrate, serial.EIGHTBITS, serial.PARITY_EVEN, serial.STOPBITS_ONE)
    #input=bytearray(address)
    #print(input)
    ser.write(b'\x9c\x9c\x1f\xc7\xbf\x78')
    ser.close()

def read():
    #ser = serial.Serial ("/dev/ttyS0", 115200, parity=serial.PARITY_EVEN)    #Open port with baud rate
    while True:
        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print (received_data)         

#open_locker(10)
#read()



    
