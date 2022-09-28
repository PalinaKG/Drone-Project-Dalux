import json
from math import pi, tan
import numpy as np

#Flight height in m
flight_height = 10 #ATH þessi verður input

#Sensor width in inches
sensor_width = 1/2.4

#Converting sensor with to mm
sensor_width *= 25.4

#Focal length in mm
focal_length = 24 # ATH þurfum að finna þessa tölu betur

#Angle of view in degrees
angle_of_view = 2*np.arctan(sensor_width / (2*focal_length)) * (180/pi)

#Field of view in m
field_of_view = 2*(tan(angle_of_view/2)*flight_height)



f = open('data.json')
data = json.load(f)
x = []
y = []


for d in data:
    x.append(d['x'])
    y.append(d['y'])


max_x = max(x)
min_x = min(x)
max_y = max(y)
min_y = min(y)

x_cur = min_x
y_cur = min_y

grid_coordinates = []

while(x_cur <= max_x):
    print("x_cur: ", x_cur)
    while(y_cur <= max_y):
        grid_coordinates.append({"x":x_cur,"y":y_cur})
        y_cur += 0.8*field_of_view
    x_cur += 0.8*field_of_view

print(grid_coordinates)




