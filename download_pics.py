from drone_commands import get_media 
import requests
import datetime

json = get_media()

print("Please input one of the following:")
print("\t a: To select all photos")
print("\t r: To select photos from most recent date")
print("\t d: To select photos from a specific date")
inp_filter = input("Enter your value: ")

while(inp_filter not in ['a', 'r', 'd']):
    inp_filter = input("Please enter a valid input [a/r/d]: ")
    
if inp_filter == 'd':
    inp_date = input("Please enter your selected date in the format dd/mm/yyyy: ")

    while(True):
        try:
            datetime.datetime.strptime(inp_date, '%d/%m/%Y')
            print('before break')
            break
        except:
            inp_date = input("Please enter valid date in the format dd/mm/yyyy: ")

inp_del = input("Would you like to delete the pictures after use? [y/n]: ")

while(inp_del not in ['y', 'n']):
    inp_del = input("Please enter a valid input [y/n]: ")

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

    new_pics = {'media_id': [], 'url' : [], 'date' : []}

    for i, date in enumerate(pics['date']):
        if date == pic_date:
            new_pics['media_id'].append(pics['media_id'][i])
            new_pics['url'].append(pics['url'][i])
            new_pics['date'].append(pics['date'][i])

    pics = new_pics            

for u in pics['url']:
    api_url = "http://192.168.42.1" + u
    response = requests.get(api_url)

    with open(u.split("/")[3], 'wb') as f:
        f.write(response.content)

if inp_del == 'y':
    print('Deleting ', len(pics['media_id']), ' photos.')
    for m in pics['media_id']:
        api_url = "http://192.168.42.1/api/v1/media/medias/" + m
        response = requests.delete(api_url)