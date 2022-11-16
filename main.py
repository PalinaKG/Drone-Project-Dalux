from shortest_path_calc import *
from drone_commands import *

flight_height = 2.

field_of_view = calc_field_of_view(flight_height=flight_height, FOV_perc=0.2)
x,y = load_GPS_data("test_data_lyngby.json")

grid_coordinates = create_GPS_grid(x,y,field_of_view)

path_coordinates = calc_shortest_path(grid_coordinates, field_of_view)

print(len(path_coordinates))

print(path_coordinates[0]['x'])

drone = olympe.Drone(DRONE_IP)
drone.connect()

drone_takeoff(drone)


calibrate_camera(drone)
align_camera(drone)
for i in range(len(path_coordinates)):
    drone_moveto(drone,path_coordinates[i]['x'], path_coordinates[i]['y'],flight_height)
    drone_take_photo(drone)

drone_moveby(mov_len=5)

land_drone(drone)
    
drone.disconnect()