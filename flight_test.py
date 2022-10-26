import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.messages.camera import take_photo, set_alignment_offsets, set_camera_mode, set_photo_mode, photo_state, alignment_offsets
from olympe.messages.common.Calibration import MagnetoCalibration
from olympe.messages.gimbal import set_target

DRONE_IP = "192.168.42.1"


list_of_coordinates = [ {'x': 55.783342468733196, 'y': 12.494245524363492},
                        {'x': 55.783342468733196, 'y': 12.49422635307005},
                        {'x': 55.783342468733196, 'y': 12.49420718177661}]

def calibrate_drone():
    drone(MagnetoCalibration(calibrate=1))

def land_drone():
    assert drone(Landing()).wait().success()

def test_takeoff():
    assert drone(TakeOff()).wait().success()
    time.sleep(10)
    assert drone(Landing()).wait().success()

def test_moveby():
    assert drone(TakeOff()).wait().success()
    drone(moveBy(1, 0, 0, 0)).wait()
    assert drone(Landing()).wait().success()

def test_moveto():
    assert drone(TakeOff()).wait().success()
    drone(moveTo(55.78306869955248, 12.49365971522669, 1, 0)).wait()
    assert drone(Landing()).wait().success()

def test_moveto_multiple():
    assert drone(TakeOff()).wait().success()
    drone(moveTo(list_of_coordinates[0]['x'], list_of_coordinates[0]['y'], 1, 0)).wait()
    drone(moveTo(list_of_coordinates[1]['x'], list_of_coordinates[1]['y'], 1, 0)).wait()
    drone(moveTo(list_of_coordinates[2]['x'], list_of_coordinates[2]['y'], 1, 0)).wait()
    assert drone(Landing()).wait().success()
    
def takePhoto():
    print("------BEFORE PHOTOSTATE------")
    drone(photo_state(cam_id=0, available=1, state=1))
    print(drone.get_state(photo_state)) 
    print("------AFTER PHOTOSTATE------")
    print("------BEFORE CAMERA MODE------")
    #if not drone(set_camera_mode(cam_id=0,value=1)).wait().success():
        #print("Set camera mode failed")
    drone(set_camera_mode(cam_id=0,value="photo")).wait()
    print("------AFTER CAMERA MODE------")
    print("------BEFORE PHOTO MODE------")
    #if not drone(set_photo_mode(cam_id=0,mode=0,format=0,file_format=0,burst=0,bracketing=0,capture_interval=0)).wait().success():
        #print("Set photo mode failed")
    drone(set_photo_mode(cam_id=0,mode=0,format=0,file_format=0,burst=0,bracketing=0,capture_interval=0)).wait()
    print("------AFTER PHOTO MODE------")
    if not drone(take_photo(cam_id=0)).wait().success():
        print("Cannot take photo")
    else:
        print("Take photo successful")
    

def test_take_photo():
    assert drone(TakeOff()).wait().success()
    takePhoto()
    assert drone(Landing()).wait().success()
    
def test_take_photo_alignment():
    #print("BEFORE FIRST PHOTO")
    assert drone(TakeOff()).wait().success()
    #takePhoto()
    #print("AFTER FIRST PHOTO")
    #alignment offset in degrees, veit ekki hvaða value við eigum að v_telja
    print("BEFORE ALIGNMENT")
    #drone(set_alignment_offsets(cam_id=0, yaw=0, pitch=90, roll=0)).wait()
    time.sleep(10)
    drone(set_target(gimbal_id=0, control_mode=0, yaw_frame_of_reference=1, yaw=0, pitch_frame_of_reference=1, pitch=-90, roll_frame_of_reference=1, roll=0)).wait().success()
    time.sleep(10)
    print("AFTER ALIGNMENT")
    print("BEFORE SECOND PHOTO")
    #takePhoto()
    print("AFTER SECOND PHOTO")
    assert drone(Landing()).wait().success()

def test_take_photo_move():
    assert drone(TakeOff()).wait().success()
    takePhoto()
    drone(moveBy(1, 0, 0, 0)).wait()
    take_photo()
    assert drone(Landing()).wait().success()

if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    #test_takeoff()
    test_take_photo_alignment()
    #land_drone()
    drone.disconnect()


