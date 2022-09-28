import folium
import json

f = open('data.json')
data = json.load(f)
x = []
y = []


for d in data:
    x.append(d['x'])
    y.append(d['y'])

print(x)
print(y)
