from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from googlemaps import Client as GoogleMaps
import requests, json, ast, random
# import fiona
# from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
import geojson
import itertools

xlsxfile = 'Pocket-Picking-Incidents-2016-2018-Sheet1.xlsx'
sheet = 'Worksheet'
# total_rows = sum(1 for line in open(xlsxfile)) - 1
# sample_size = 38
# print total_rows
# skip = sorted(random.sample(xrange(1, total_rows + 1), total_rows - sample_size))
data = pd.read_excel(xlsxfile, sheet_name=sheet)



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
# print crime_types

# # array to store modified addresses
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
# with open('Incidents 2016 to 2018 copy.csv', 'r') as csvinput:
# 	with open('output_test.csv', 'w') as csvoutput:
# 		writer = csv.writer(csvoutput, lineterminator='\n')
# 		reader = csv.reader(csvinput)

# 		all = []
# 		row = next(reader)
# 		row.append('X COORDINATES')
# 		row.append('Y COORDINATES')
# 		all.append(row)

# 		i = 0
# 		for row in reader:
# 			row.append(x_coordinates[i])
# 			row.append(y_coordinates[i])
# 			all.append(row)
# 			i += 1

# 		writer.writerows(all)

x_coordinates_col = []
y_coordinates_col = []

for i in range(len(x_coordinates)):
	x_coordinates_col.append([x_coordinates[i]])
np_x_coordinates_col = np.array(x_coordinates_col)
print np_x_coordinates_col

for i in range(len(y_coordinates)):
	y_coordinates_col.append([y_coordinates[i]])
np_y_coordinates_col = np.array(y_coordinates_col)
print np_y_coordinates_col

pd_coordinates_col = pd.DataFrame({'X_Coordinates':np_x_coordinates_col[:,0], 'Y_Coordinates':np_y_coordinates_col[:,0]})
# pd_y_coordinates_col = pd.DataFrame({'Y_Coordinates':np_y_coordinates_col[:,0]})
print pd_coordinates_col
# print pd_y_coordinates_col

to_update = {sheet : pd_coordinates_col}

# load existing data
excel_reader = pd.ExcelFile(xlsxfile)

# write and update
excel_writer = pd.ExcelWriter(xlsxfile)

for sheet in excel_reader.sheet_names:
	sheet_df = excel_reader.parse(sheet)
	append_df =  to_update.get(sheet)

	if append_df is not None:
		sheet_df = pd.concat([sheet_df, append_df], axis=1)

	sheet_df.to_excel(excel_writer, sheet, index=False)
excel_writer.save()

'''
Get coordinates from x_coordinates and y_coordinates array
and place in a .csv file
'''
# formatted_coordinates = np.asarray( [x_coordinates, y_coordinates])
# print(formatted_coordinates)

# with open('output_test.csv', 'w') as f:
# 	f.write('X_COORDINATES,Y_COORDINATES\n')
# 	count = 0
# 	for i in range(len(x_coordinates)):
# 		for j in range(len(y_coordinates)):
# 			output = str(x_coordinates[i]) + ',' + str(y_coordinates[count]) + '\n'
# 			f.write(output)
# 			count = count + 1
# 			break

	
# np.savetxt("output_test.csv", formatted_coordinates, delimiter=",")
# pd.DataFrame(formatted_coordinates).to_csv("output_test.csv")

# # geolocator = Nominatim()
# # location = geolocator.geocode("41ST ST / JEFFERSON AVE")
# # print location.latitude, location.longitude

 
# map = Basemap(projection='merc', lat_0 = 36.9786449, lon_0 = -76.4321089,
#     resolution = 'h', area_thresh = 0.1,
#     llcrnrlon=-77.1, llcrnrlat=36.7,
#     urcrnrlon=-75.3, urcrnrlat=38)
 
# map.drawcoastlines()
# map.drawcountries()
# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color = 'coral')
# map.drawmapboundary()

# patches = []

# map.readshapefile('ZoningDistrict/ZoningDistrict_test_2', 'ZoningDistrict_test_2')
# map.readshapefile('RoadCenterlines/RoadCenterlines_2', 'RoadCenterlines_2')
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
# x,y = map(x_coordinates, y_coordinates)

# counter = 0
# for crimes in crime_types:
# 	if (crimes == 'POCKET PICKING'):
# 		# print 'drug/narcotics'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='green')
# 	if (crimes == 'SIMPLE ASSAULT'):
# 		# print 'simple assault'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='blue')
# 	if (crimes == 'CURFEW'):
# 		# print 'curfew'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='red')
# 	if (crimes == 'WEAPON OFFENSE'):
# 		# print 'weapon offense'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='orange')
# 	if (crimes == 'AGGRAVATED ASSAULT'):
# 		# print 'aggravated assault'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='green')
# 	if (crimes == 'THEFT FROM BUILDING'):
# 		# print 'theft from building'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='yellow')
# 	if (crimes == 'ROBBERY'):
# 		# print 'robbery'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='m')
# 	if (crimes == 'DAMAGE PROPERTY'):
# 		# print 'damage property'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='black')
# 	if (crimes == 'LEAVING THE SCENE'):
# 		# print 'leaving the scene'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='white')
# 	if (crimes == 'JUVENILE - RUNAWAY'):
# 		# print 'juvenile - runaway'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='purple')
# 	if (crimes == 'LARCENY'):
# 		# print 'larceny'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='gray')
# 	if (crimes == 'THEFT FROM VEHICLE'):
# 		# print 'theft from vehicle'
# 		map.plot(x[counter], y[counter], 'bo', markersize=4, color='pink')


# 	counter += 1

 
# plt.show()