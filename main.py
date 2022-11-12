from shortest_path_calc import *
from fly_drone import *

# flight_height = 2.

# field_of_view = calc_field_of_view(flight_height=flight_height, FOV_perc=0.2)
# x,y = load_GPS_data("test_data_lyngby.json")

# grid_coordinates = create_GPS_grid(x,y,field_of_view)

# path_coordinates = calc_shortest_path(grid_coordinates, field_of_view)

# print(len(path_coordinates))

# print(path_coordinates[0]['x'])

#drone = olympe.Drone(DRONE_IP)
#drone.connect()

# drone_takeoff(drone)


# calibrate_camera(drone)
# align_camera(drone)
# for i in range(len(path_coordinates)):
#     drone_moveto(drone,path_coordinates[i]['x'], path_coordinates[i]['y'],flight_height)
#     drone_take_photo(drone)

# drone_moveby(mov_len=5)

# land_drone(drone)
# f = open('photo_data.json')
# json = json.load(f)
json = get_media()


print("Please input one of the following:")
print("\t a: To select all photos")
print("\t r: To select photos from most recent date")
print("\t d: To select photos from a specific date")
inp_filter = input("Enter your value: ")

if inp_filter == 'd':
    inp_date = input("Please enter your selected date in the format dd/mm/yyyy: ")

inp_del = input("Would you like to delete the pictures after use? [y/n]: ")

pics = {'media_id': [], 'url' : [], 'date' : []}

for item in json:
    if not item['type'] == 'VIDEO':
        pics['media_id'].append(item['media_id'])
        pics['url'].append(item['resources'][0]['url'])
        pics['date'].append(item['datetime'].split("T")[0])


if not inp_filter == 'a':
    if inp_filter == 'r':
        pic_date = max(pics['date'])
    elif inp_filter == 'd':
        inp_split = inp_date.split("/")
        pic_date = inp_split[2] + inp_split[1] + inp_split[0]

    print("pic date: ", pic_date)

    print(pics['date'])

    new_pics = {'media_id': [], 'url' : [], 'date' : []}

    for i, date in enumerate(pics['date']):
        if date == pic_date:
            new_pics['media_id'].append(pics['media_id'][i])
            new_pics['url'].append(pics['url'][i])
            new_pics['date'].append(pics['date'][i])

    pics = new_pics            
print(pics['date'])

for u in pics['url']:
    api_url = "http://192.168.42.1" + u
    response = requests.get(api_url)

    with open(u.split("/")[3], 'wb') as f:
        f.write(response.content)

if inp_del == 'y':
    print("deleting")
    for m in pics['media_id']:
        api_url = "http://192.168.42.1/api/v1/media/medias/" + m
        response = requests.delete(api_url)
        print(response)

#print(json[4])



# # with open('photo_data.json', 'w') as f:
# #     f.write(str(json))
    
# #drone.disconnect()