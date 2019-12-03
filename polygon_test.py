from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from googlemaps import Client as GoogleMaps
import requests, json, ast, random
import fiona
from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
import geojson

filename = 'Incidents 2016 to 2018.csv'
# total_rows = sum(1 for line in open(filename)) - 1
# sample_size = 5
# print total_rows
# skip = sorted(random.sample(xrange(1, total_rows + 1), total_rows - sample_size))
# data = pd.read_csv(filename, skiprows=skip)

data = pd.read_csv(filename)



'''
***************************************
Using GoogleMaps
***************************************
'''
gmaps = GoogleMaps('AIzaSyDAQjEueKtHkby1KhCto7dD4GVnG4bPGTM')

# This is an example 
# address = '3100 MADISON AVE, Newport News'
# result = gmaps.geocode(address)
# print result[0]['geometry']['location']

# response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')

# resp_json_payload = response.json()

# print resp_json_payload



'''
***************************************
Using requests
***************************************
'''
# url = 'http://photon.komoot.de/api/?q='
# addresses = ['175 5th Avenue NYC', 'Constitution Ave NW & 10th St NW, Washington, DC']

# for address in addresses:
#     resp = requests.get(url=url+address)
#     data = json.loads(resp.text)
#     print data['features'][0]['geometry']['coordinates']



'''
***************************************
Using GeoLocator
***************************************
'''
# geolocator = Nominatim()

a = data['ADDRESS'].values
crime_types = data['OFFENSE'].values
print crime_types

# array to store modified addresses
new_addresses = []
x_coordinates = []
y_coordinates = []

count = 0
for x in a[:]:
	if "BLK" in x:
		new_string = x.replace(" BLK", "")
		new_addresses.append(new_string + ', Newport News, VA')
		# location = geolocator.geocode(new_string)
		# x_coordinates.append(location.longitude)
		# y_coordinates.append(location.latitude)
		location = gmaps.geocode(new_string + ', Newport News, VA')
		x_coordinates.append(location[0]['geometry']['location']['lng'])
		y_coordinates.append(location[0]['geometry']['location']['lat'])
		print count, new_string, location[0]['geometry']['location']['lng'], location[0]['geometry']['location']['lat']
		count += 1
	elif "/ ORCUTT" in x:
		new_string = x.replace(" / ORCUTT", "")
		new_addresses.append(new_string + ', Newport News, VA')
		# location = geolocator.geocode(new_string)
		# x_coordinates.append(location.longitude)
		# y_coordinates.append(location.latitude)
		location = gmaps.geocode(new_string + ', Newport News, VA')
		x_coordinates.append(location[0]['geometry']['location']['lng'])
		y_coordinates.append(location[0]['geometry']['location']['lat'])
		print count, new_string, location[0]['geometry']['location']['lng'], location[0]['geometry']['location']['lat']
		count += 1
	else:
		new_addresses.append(x + ', Newport News, VA')
		# location = geolocator.geocode(new_string)
		# x_coordinates.append(location.longitude)
		# y_coordinates.append(location.latitude)
		location = gmaps.geocode(x + ', Newport News, VA')
		x_coordinates.append(location[0]['geometry']['location']['lng'])
		y_coordinates.append(location[0]['geometry']['location']['lat'])
		print count, x, location[0]['geometry']['location']['lng'], location[0]['geometry']['location']['lat']
		count += 1

print new_addresses



# f = open('Incidents 2016 to 2018 copy.csv')
# numlines = len(f.readlines())

# print len(x_coordinates)
# print numlines

# '''
# Reads lines from csv and outputs to another csv file

# '''

with open('Incidents 2016 to 2018.csv', 'r') as csvinput:
	with open('output_test.csv', 'w') as csvoutput:
		writer = csv.writer(csvoutput, lineterminator='\n')
		reader = csv.reader(csvinput)

		all = []
		row = next(reader)
		# row.append('X COORDINATES')
		# row.append('Y COORDINATES')
		all.append(row)

		i = 0
		for row in reader:
			# row.append(x_coordinates[i])
			# row.append(y_coordinates[i])
			all.append(row)
			i += 1

		writer.writerows(all)


# # geolocator = Nominatim()
# # location = geolocator.geocode("41ST ST / JEFFERSON AVE")
# # print location.latitude, location.longitude

 
map = Basemap(projection='merc', lat_0 = 36.9786449, lon_0 = -76.4321089,
    resolution = 'h', area_thresh = 0.1,
    llcrnrlon=-77.1, llcrnrlat=36.7,
    urcrnrlon=-75.3, urcrnrlat=38)
 
map.drawcoastlines()
map.drawcountries()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color = 'coral')
map.drawmapboundary()

patches = []

map.readshapefile('ZoningDistrict/ZoningDistrict_test_2', 'ZoningDistrict_test_2')
# for info, shape in zip(map.ZoningDistrict_test_2_info, map.ZoningDistrict_test_2):
# 	print info

# with open("ZoningDistrict/ZoningDistrict_Points.geojson") as json_file:
# 	json_data = geojson.load(json_file)	
# 	print json_data
	

# multipol = fiona.open('ZoningDistrict/ZoningDistrict_test_2.shp')
# multi = multipol.next()
# print multi
# for i in range(20):
# 	map.plot(multi['geometry']['coordinates'][i][1], multi['geometry']['coordinates'][i][0], 'bo', markersize=4, color='green')
# 	print multi['geometry']['coordinates'][i][1], multi['geometry']['coordinates'][i][0]
# print multi['geometry']['coordinates'][0][0]
# map.plot(multi['geometry']['coordinates'][0][0], multi['geometry']['coordinates'][0][1], 'bo', markersize=4, color='blue')
# map.plot(multi['geometry']['coordinates'][1][0], multi['geometry']['coordinates'][1][1], 'bo', markersize=4, color='blue')
# map.plot(multi['geometry']['coordinates'][2][0], multi['geometry']['coordinates'][2][1], 'bo', markersize=4, color='blue')



# lons = [-76.9, -76.2, -76.4]
# lats = [36.2, 36.4, 36.9]
x,y = map(x_coordinates, y_coordinates)

# counter = 0
# for crimes in crime_types:
# 	if (crimes == 'DRUG/NARCOTICS OFFENSES'):
# 		# print 'drug/narcotics'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='aqua')
	


	# counter += 1

 
plt.show()