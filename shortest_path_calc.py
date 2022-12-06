import json
from math import pi, tan, cos, inf
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import networkx as nx
import networkx.algorithms.approximation as nx_app
import geopy.distance as geo_dist

def calc_field_of_view_old(flight_height, FOV_perc=0.8):
    #Flight height in m
    flight_height = flight_height #ATH þessi verður input

    #Sensor width in inches
    sensor_width = 1/2.4

    #Converting sensor with to mm
    sensor_width *= 25.4

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

def calc_field_of_view_GPS(flight_height, first_lat, FOV_perc=0.2):
    #Flight height in m
    flight_height = flight_height

    #Angle of view in radians
    v_aov = 56.625 * pi / 180
    h_aov = 75.5 * pi / 180

    #Field of view in m
    v_fov = abs(2*(tan(v_aov/2)*flight_height))
    h_fov = abs(2*(tan(h_aov/2)*flight_height))

    #Using only smaller dimensions
    fov = min(v_fov,h_fov)
    fov *= FOV_perc

    #Convert to GPS coordinates
    lat_fov = fov / 111139
    lon_fov = fov / (111139  * cos(first_lat * pi/180))

    return lat_fov, lon_fov

def calc_field_of_view_m(flight_height, FOV_perc=0.2):
    #Flight height in m
    flight_height = flight_height

    #Angle of view in degrees
    v_aov = 56.625 * pi / 180
    h_aov = 75.5 * pi / 180

    #Field of view in m
    v_fov = abs(2*(tan(v_aov/2)*flight_height))
    h_fov = abs(2*(tan(h_aov/2)*flight_height))

    #Using only smaller dimensions
    fov = min(v_fov,h_fov)
    fov *= FOV_perc

    return fov


def load_GPS_data(file_name):
    f = open(file_name)
    data = json.load(f)

    x = []
    y = []


    for d in data:
        x.append(d['x'])
        y.append(d['y'])
    
    return x,y

def create_GPS_grid(x,y,lat_fov,lon_fov,fov_m):
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
            y_cur += lon_fov
        x_cur += lat_fov


    G = nx.Graph()

    for idx, coordinate in enumerate(grid_coordinates):
        G.add_node(idx, is_full=0, coordinate=coordinate)
        
    max_dist = np.sqrt(2*(fov_m**2)) + (0.1*fov_m)
    G2 = G.copy()
    for node in G:
        G2.remove_node(node)
        for node2 in G2:
            dist = geo_dist.geodesic((G.nodes[node]['coordinate']['x'],G.nodes[node]['coordinate']['y']), 
                            (G2.nodes[node2]['coordinate']['x'],G2.nodes[node2]['coordinate']['y'])).m
            if dist <= max_dist:
                G.add_edge(node, node2, weight = dist)
    
    return G

def calc_shortest_path(G,start):

    start_node = find_start_node(G,start)

    method = lambda G, source=start_node : nx_app.greedy_tsp(G, source=start_node)
    path = nx_app.traveling_salesman_problem(G,method=method)

    list_of_coordinates = []
    for node in path:
        list_of_coordinates.append(G.nodes[node]['coordinate'])

    return list_of_coordinates

def find_start_node(G,start):
    #Find node closest to start (used in greedy_tsp algorithm)
    min_dist = inf
    for node in G.nodes:
        dist = geo_dist.geodesic(start, (G.nodes[node]['coordinate']['x'],G.nodes[node]['coordinate']['y'])).m
        if dist < min_dist:
            min_dist = dist
            min_node = node
        
    return min_node







