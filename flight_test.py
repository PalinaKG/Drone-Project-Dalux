import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.messages.camera import take_photo, set_alignment_offsets, set_camera_mode, set_photo_mode, photo_state, alignment_offsets
from olympe.messages.common.Calibration import MagnetoCalibration
from olympe.messages.gimbal import set_target, attitude
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged, GPSFixStateChanged

from drone_commands import *
from shortest_path_calc import *

DRONE_IP = "192.168.42.1"


list_of_coordinates = [ {'x': 55.783342468733196, 'y': 12.494245524363492},
                        {'x': 55.783342468733196, 'y': 12.49422635307005},
                        {'x': 55.783342468733196, 'y': 12.49420718177661}]

# def calibrate_drone():
#     drone(MagnetoCalibration(calibrate=1))

# def land_drone():
#     assert drone(Landing()).wait().success()

# def test_takeoff():
#     assert drone(TakeOff()).wait().success()
#     time.sleep(10)
#     assert drone(Landing()).wait().success()

# def test_moveby():
#     assert drone(TakeOff()).wait().success()
#     drone(moveBy(1, 0, 0, 0)).wait()
#     assert drone(Landing()).wait().success()

# def test_moveto():
#     assert drone(TakeOff()).wait().success()
#     drone(moveTo(55.78306869955248, 12.49365971522669, 1, 0)).wait()
#     assert drone(Landing()).wait().success()

# def test_moveto_multiple():
#     assert drone(TakeOff()).wait().success()
#     drone(moveTo(list_of_coordinates[0]['x'], list_of_coordinates[0]['y'], 1, 0)).wait()
#     drone(moveTo(list_of_coordinates[1]['x'], list_of_coordinates[1]['y'], 1, 0)).wait()
#     drone(moveTo(list_of_coordinates[2]['x'], list_of_coordinates[2]['y'], 1, 0)).wait()
#     assert drone(Landing()).wait().success()
    
# def takePhoto():
#     print("------BEFORE PHOTOSTATE------")
#     drone(photo_state(cam_id=0, available=1, state=1))
#     print(drone.get_state(photo_state)) 
#     print("------AFTER PHOTOSTATE------")
#     print("------BEFORE CAMERA MODE------")
#     #if not drone(set_camera_mode(cam_id=0,value=1)).wait().success():
#         #print("Set camera mode failed")
#     drone(set_camera_mode(cam_id=0,value="photo")).wait()
#     print("------AFTER CAMERA MODE------")
#     print("------BEFORE PHOTO MODE------")
#     #if not drone(set_photo_mode(cam_id=0,mode=0,format=0,file_format=0,burst=0,bracketing=0,capture_interval=0)).wait().success():
#         #print("Set photo mode failed")
#     drone(set_photo_mode(cam_id=0,mode=0,format=0,file_format=0,burst=0,bracketing=0,capture_interval=0)).wait()
#     print("------AFTER PHOTO MODE------")
#     if not drone(take_photo(cam_id=0)).wait().success():
#         print("Cannot take photo")
#     else:
#         print("Take photo successful")
    

# def test_take_photo():
#     assert drone(TakeOff()).wait().success()
#     takePhoto()
#     assert drone(Landing()).wait().success()
    
# def test_take_photo_alignment():
#     #print("BEFORE FIRST PHOTO")
#     assert drone(TakeOff()).wait().success()
#     #takePhoto()
#     #print("AFTER FIRST PHOTO")
#     #alignment offset in degrees, veit ekki hvaða value við eigum að v_telja
#     print("BEFORE ALIGNMENT")
#     #drone(set_alignment_offsets(cam_id=0, yaw=0, pitch=90, roll=0)).wait()
#     time.sleep(5)
#     drone(set_target(gimbal_id=0, control_mode=0, yaw_frame_of_reference=1, yaw=0, pitch_frame_of_reference=1, pitch=-90, roll_frame_of_reference=1, roll=0)).wait().success()
    
#     print("Attitude before: ", drone.get_state(attitude)[0]["pitch_relative"]) 
#     while (drone.get_state(attitude)[0]["pitch_relative"] != -90):
#         time.sleep(1)
#         print("Attitude: ", drone.get_state(attitude)[0]["pitch_relative"]) 
    
#     time.sleep(5)
#     print("AFTER ALIGNMENT")
#     print("BEFORE SECOND PHOTO")
#     #takePhoto()
#     print("AFTER SECOND PHOTO")
#     assert drone(Landing()).wait().success()

# def test_take_photo_move():
#     assert drone(TakeOff()).wait().success()
#     takePhoto()
#     drone(moveBy(1, 0, 0, 0)).wait()
#     take_photo()
#     assert drone(Landing()).wait().success()

if __name__ == "__main__":
    flight_height = 5.
    field_of_view = calc_field_of_view_m(flight_height=flight_height, FOV_perc=0.2)

    print(field_of_view)

    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    
    # drone_takeoff(drone,flight_height)

    # calibrate_camera(drone)
    # align_camera(drone)

    # drone_take_photo(drone)

    # for i in range(6,15):
    #     print("NEW I:", i)
    #     drone(moveBy(field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # print("MOVE RIGHT 1")

    # drone(moveBy(0, field_of_view, 0, 0)).wait()
    # drone_take_photo(drone)

    # for i in range(0,15):
    #     print("NEW I:", i)
    #     drone(moveBy(-field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # print("MOVE RIGHT 2")

    # drone(moveBy(0, field_of_view, 0, 0)).wait()
    # drone_take_photo(drone)

    # for i in range(0,15):
    #     print("NEW I:", i)
    #     drone(moveBy(field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # print("MOVE RIGHT 3")

    # drone(moveBy(0, field_of_view, 0, 0)).wait()
    # drone_take_photo(drone)

    # for i in range(0,15):
    #     print("NEW I:", i)
    #     drone(moveBy(-field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)


    # for i in range(0,15):
    #     drone(moveBy(field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # for j in range(0,7):
    #     print("STARTING NEW J:",j)
    #     drone(moveBy(0, field_of_view, 0, 0)).wait()
    #     drone_take_photo(drone)

    #     if j in [0,2,4,6]:
    #         for i in range(0,15):
    #             print("NEW I:", i)
    #             drone(moveBy(-field_of_view, 0, 0, 0)).wait()
    #             drone_take_photo(drone)
    #     else:
    #         for i in range(0,15):
    #             print("NEW I:", i)
    #             drone(moveBy(field_of_view, 0, 0, 0)).wait()
    #             drone_take_photo(drone)

    # print("FOR LOOP DONE")

    # for i in range(0,3):
    #     drone(moveBy(-field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # drone(moveBy(0, field_of_view, 0, 0)).wait()
    # drone_take_photo(drone)


    # for i in range(0,3):
    #     drone(moveBy(field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)

    # drone(moveBy(0, field_of_view, 0, 0)).wait()
    # drone_take_photo(drone)

    # for i in range(0,3):
    #     drone(moveBy(-field_of_view, 0, 0, 0)).wait()
    #     drone_take_photo(drone)


    #drone(moveBy(2, 0, 0, 0)).wait()
    # drone(GPSFixStateChanged(_policy = 'wait'))

    # GPS_state = drone.get_state(HomeChanged)

    # starting_node = (GPS_state["latitude"], GPS_state["longitude"])

    # print("GPS position before take-off : lat =", starting_node[0], "lon =", starting_node[1])


    land_drone(drone)
    drone.disconnect()



