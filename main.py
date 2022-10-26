from shortest_path_calc import *


field_of_view = calc_field_of_view(flight_height=2.)
x,y = load_GPS_data("test_data_lyngby.json")

grid_coordinates = create_GPS_grid(x,y,field_of_view)

path_coordinates = calc_shortest_path(grid_coordinates, field_of_view)

print(len(path_coordinates))