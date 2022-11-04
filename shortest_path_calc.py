import json
from math import pi, tan
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import networkx as nx
import networkx.algorithms.approximation as nx_app

def calc_field_of_view_old(flight_height, FOV_perc=0.8):
    #Flight height in m
    flight_height = flight_height #ATH þessi verður input

    #Sensor width in inches
    sensor_width = 1/2.4

    #Converting sensor with to mm
    sensor_width *= 25.4
    print(sensor_width)

    #Focal length in mm
    #focal_length = 24 # ATH þurfum að finna þessa tölu betur
    focal_length = 25 # ATH þurfum að finna þessa tölu betur

    #Angle of view in degrees
    angle_of_view = 2*np.arctan(sensor_width / (2*focal_length)) * (180/pi)

    #Field of view in m
    field_of_view = abs(2*(tan(angle_of_view/2)*flight_height))
    print(field_of_view)

    #Convert to GPS coordinates
    field_of_view /= 111139

    #Only use the allotted percentage of the field of view
    field_of_view *= FOV_perc

    return field_of_view

def calc_field_of_view(flight_height, FOV_perc=0.8):
    #Flight height in m
    flight_height = flight_height #ATH þessi verður input

    #Angle of view in degrees
    v_aov = 56.625 * pi / 180
    h_aov = 75.5 * pi / 180

    #Field of view in m
    v_fov = abs(2*(tan(v_aov/2)*flight_height))
    h_fov = abs(2*(tan(h_aov/2)*flight_height))

    #Convert to GPS coordinates
    v_fov /= 111139
    h_fov /= 111139

    #Only use the allotted percentage of the field of view
    v_fov *= FOV_perc
    h_fov *= FOV_perc

    return h_fov


def load_GPS_data(file_name):
    f = open(file_name)
    data = json.load(f)

    x = []
    y = []


    for d in data:
        x.append(d['x'])
        y.append(d['y'])
    
    return x,y

def create_GPS_grid(x,y, field_of_view):
    max_x = max(x)
    min_x = min(x)
    max_y = max(y)
    min_y = min(y)

    x_cur = min_x
    y_cur = min_y

    grid_coordinates = []


    new_tuple = [(x[idx],y[idx]) for idx in range(len(x))]
    polygon = Polygon(new_tuple)
    first = True
    while(x_cur <= max_x):
        y_cur = min_y
        while(y_cur <= max_y):
            point2 = Point(x_cur ,y_cur)
            if polygon.contains(point2):
                grid_coordinates.append({"x":x_cur,"y":y_cur})
            y_cur += field_of_view
        x_cur += field_of_view
    
    return grid_coordinates

def calc_shortest_path(grid_coordinates, field_of_view):

    G = nx.Graph()

    for idx, coordinate in enumerate(grid_coordinates):
        G.add_node(idx, is_full=0, coordinate=coordinate)
        
    max_dist = np.sqrt(2*(field_of_view**2))
    G2 = G.copy()
    for node in G:
        G2.remove_node(node)
        for node2 in G2:
            x_dist = abs(G.nodes[node]['coordinate']['x'] - G2.nodes[node2]['coordinate']['x'])
            y_dist = abs(G.nodes[node]['coordinate']['y'] - G2.nodes[node2]['coordinate']['y'])
            if (x_dist <= max_dist and y_dist <= max_dist):
                G.add_edge(node, node2, weight = np.sqrt(x_dist**2 + y_dist**2))


    path = nx_app.traveling_salesman_problem(G, cycle=False)

    list_of_coordinates = []
    for node in path:
        list_of_coordinates.append(G.nodes[node]['coordinate'])

    return list_of_coordinates







