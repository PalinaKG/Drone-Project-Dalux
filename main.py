from shortest_path_calc import *
from drone_commands import *
from olympe.messages.ardrone3.GPSSettingsState import HomeChanged

# Setting the altitude for the drone to fly, in meters
flight_height = 10.0

# Calculating field of view and creating the GPS grid
x,y = load_GPS_data("data.json")
lat_fov, lon_fov = calc_field_of_view_GPS(flight_height=flight_height, FOV_perc=0.2, first_lat=x[0])
fov_m = calc_field_of_view_m(flight_height=flight_height)
grid_coordinates = create_GPS_grid(x,y,lat_fov,lon_fov,fov_m)

# Connecting to drone and getting the inital location
drone = olympe.Drone(DRONE_IP)
drone.connect()

# GPS_state = drone.get_state(HomeChanged)
# start = (GPS_state["latitude"], GPS_state["longitude"])


# # Calculating shortest path
# path_coordinates = calc_shortest_path(grid_coordinates,start)

# # Initalizing all unique coordinates as not photographed

# unique_coords = []
# for coord in path_coordinates:
#     if coord not in unique_coords:
#         unique_coords.append(coord)

# photographed_coords = {'coordinate': unique_coords, 'photographed': [0]*len(unique_coords)}

# # Send instructions to drone to take off, calibrate and align the camera
# drone_takeoff(drone, flight_height)
# calibrate_camera(drone)
# align_camera(drone)

# # Loop through all coordinates in the path and take photos
# for i, coord in enumerate(path_coordinates):
#     drone_moveto(drone,path_coordinates[i]['x'], path_coordinates[i]['y'],flight_height)

#     # We only want to take a photo if node is not being revisited
#     if not photographed_coords['photographed'][photographed_coords['coordinate'].index(coord)]:
#         drone_take_photo(drone)
#         photographed_coords['photographed'][photographed_coords['coordinate'].index(coord)] = 1

# # Make drone return to original pos 
# drone_return(drone)

# Land drone and disconnect
land_drone(drone)
drone.disconnect()
