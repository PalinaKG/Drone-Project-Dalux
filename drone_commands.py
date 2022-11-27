import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.messages.camera import take_photo, set_alignment_offsets, set_camera_mode, set_photo_mode, photo_state, alignment_offsets
from olympe.messages.common.Calibration import MagnetoCalibration
from olympe.messages.gimbal import set_target, attitude
import requests

DRONE_IP = "192.168.42.1"


def land_drone(drone):
    assert drone(Landing()).wait().success()

def drone_takeoff(drone, flight_height):
    assert drone(TakeOff()).wait().success()
    drone(moveBy(0, 0, 1-flight_height, 0)).wait()
    time.sleep(2)

def drone_moveto(drone,lat,lon,height):
    drone(moveTo(latitude=lat, longitude=lon, altitude=height, orientation_mode=0,heading=0)).wait()
    time.sleep(1)

def drone_moveby(drone, mov_len):
    drone(moveBy(mov_len, 0, 0, 0)).wait()

def calibrate_camera(drone):
    drone(photo_state(cam_id=0, available=1, state=1))
    drone(set_camera_mode(cam_id=0,value="photo")).wait()
    drone(set_photo_mode(cam_id=0,mode=0,format=1,file_format=0,burst=0,bracketing=0,capture_interval=0)).wait()

def drone_take_photo(drone):
    time.sleep(0.5)
    if not drone(take_photo(cam_id=0)).wait().success():
        print("Cannot take photo")
    else:
        print("Take photo successful")
    time.sleep(0.5)
    
def align_camera(drone):
    drone(set_target(gimbal_id=0, control_mode=0, yaw_frame_of_reference=1, yaw=0, pitch_frame_of_reference=1, pitch=-90, roll_frame_of_reference=1, roll=0)).wait().success()
    
    while (drone.get_state(attitude)[0]["pitch_relative"] != -90):
        time.sleep(1)



def get_media():
    api_url = "http://192.168.42.1/api/v1/media/medias"
    response = requests.get(api_url)
    return response.json()