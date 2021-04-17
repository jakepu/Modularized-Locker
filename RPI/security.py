from paramiko import SSHClient
from scp import SCPClient
from gpiozero import MotionSensor
from picamera import PiCamera
import os
import sys
from datetime import datetime
saved_path = '/home/pi/images'

def capture_upload(camera):
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    img_filepath = saved_path + '/' + date + '.jpg'
    camera.capture(img_filepath)
    with SSHClient() as ssh:
        ssh.connect(hostname = '98.212.157.222', username='locker', passwork='ECE 445 Team 61')
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(img_filepath, remote_path='/home/locker')
        


def main():
    pir = MotionSensor(4)
    camera = PiCamera()
    try:
        os.mkdir(saved_path)
    except FileExistsError:
        pass
    except OSError:
        sys.exit('Failed to find/create a directory to save images. File path:', saved_path)
    while True:
        pir.wait_for_motion(timeout=None)
        capture_upload(camera)

