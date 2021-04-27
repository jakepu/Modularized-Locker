from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
from gpiozero import MotionSensor
from picamera import PiCamera
import os
import sys
from datetime import datetime
import time
saved_path = '/home/pi/images'

def capture_upload(camera):
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    img_filepath = saved_path + '/' + date + '.jpg'
    camera.capture(img_filepath)
    # with SSHClient() as ssh:
    #     ssh.set_missing_host_key_policy(AutoAddPolicy())
    #     ssh.connect(hostname = '98.212.157.222', username='locker', password='ECE 445 Team 61')
    #     with SCPClient(ssh.get_transport()) as scp:
    #         scp.put(img_filepath, remote_path='/home/locker')
        


def main():
    pir = MotionSensor(12)
    camera = PiCamera()
    try:
        os.mkdir(saved_path)
    except FileExistsError:
        pass
    except OSError:
        sys.exit('Failed to find/create a directory to save images. File path:', saved_path)
    while True:
        time.sleep(5)
        pir.wait_for_motion(timeout=None)
        capture_upload(camera)
