import olympe
import os
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo

DRONE_IP = "192.168.42.1"


list_of_coordinates = [ {'x': 55.783342468733196, 'y': 12.494245524363492},
                        {'x': 55.783342468733196, 'y': 12.49422635307005},
                        {'x': 55.783342468733196, 'y': 12.49420718177661}]


def test_takeoff():
    assert drone(TakeOff()).wait().success()
    time.sleep(10)
    assert drone(Landing()).wait().success()

def test_moveby():
    assert drone(TakeOff()).wait().success()
    drone(moveBy(10, 0, 0, 0)).wait()
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

if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    test_takeoff()
    drone.disconnect()


