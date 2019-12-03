#####################################################################
#				Imports 				 							#
#####################################################################
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
#import numpy.ndarray
import pandas as pd
from googlemaps import Client as GoogleMaps
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.collections import PatchCollection
import geopandas as gdp
import fiona
from shapely.geometry import Point as shapelyPoint
from shapely.geometry import LineString
from shapely.geometry.polygon import Polygon as shapelyPolygon

#xlsxfile 	= 'Incidents 2016 to 2018 no dups.xlsx'
#xlsxfile	= 'Book4.xlsx'
#filename 	= 'Incidents 2016 to 2018.csv'
xlsxfile 	= 'Incidents by Offense 2016 to 2018.xlsx'
sheet		= 'Pocket Picking'

data = pd.read_excel(xlsxfile, sheet_name=sheet)
#data = pd.read_excel(xlsxfile)
gmaps = GoogleMaps('AIzaSyDAQjEueKtHkby1KhCto7dD4GVnG4bPGTM')

a = data['ADDRESS'].values


#####################################################################
#				Determine the (lat, lon) of each address			#
#####################################################################
print '\nHERE ARE THE ADDRESSES:..............' 
new_addresses = []
x_coordinates = []
y_coordinates = []
address_zones = []
count = 0
for x in a[:]:
	if "BLK" in x:
		new_string = x.replace(" BLK", "")
#	elif "/ ORCUTT" in x:
#		new_string = x.replace(" / ORCUTT", "")
	else:
		new_string = x
	new_string = new_string + ', Newport News, VA'
	new_addresses.append(new_string)
	location = gmaps.geocode(new_string)
	x_coordinates.append(location[0]['geometry']['location']['lng'])
	y_coordinates.append(location[0]['geometry']['location']['lat'])
	print count,'\t', new_string, '\t',location[0]['geometry']['location']['lng'], '\t',location[0]['geometry']['location']['lat']
	count+=1

print '\nProcessing Map Image........\t'
fig, ax = plt.subplots()
# (-76.62686736643403, 36.960797041307146, -76.3876260594103, 37.22066807617356)
map = Basemap(projection='merc', lat_0 = 36.9786449, lon_0 = -76.4321089,
    resolution ='l', area_thresh = 0.1,
    llcrnrlon=-76.62686736643403, llcrnrlat=36.96079704130714,
    urcrnrlon=-76.3876260594103, urcrnrlat=37.22066807617356)
map.drawcoastlines()
map.drawcountries()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color = 'dimgrey',lake_color='aqua')
patches = []


#####################################################################
#				Add Zones shapefile to map 							#
#####################################################################
map.readshapefile('ZoningDistrict/ZoningDistrict_test_2', 
	'ZoningDistrict_test_2', drawbounds = False)

# df_poly = pd.DataFrame({
# 	'shapes': [mplPolygon(np.array(shape), True) for shape in map.ZoningDistrict_test_2],
# 	'area:' : [ZoningDistrict_test_2['name'] for ZoningDistrict_test_2 in map.ZoningDistrict_test_2_info]
# 	})
# print df_poly;

#####################################################################
#  				Add colors to each zone 							#
#  																	#
# Colors: https://matplotlib.org/examples/color/named_colors.html	#
#  ZONECLASS == R1, R2, R3, R4, R5, R6, R7, R8, R9					#
# 			 == C1, C2, C3, C4, C5, O1, O2, O3						#
#			 == M1, M2, M3, P1, OVERLAY								#
#  This for loop defines the colors of each zone 					#
#####################################################################
#for info, shape in zip(map.ZoningDistrict_test_2_info, map.ZoningDistrict_test_2):
#	print 'RINGNUM: ',info['RINGNUM'],'\t','SHAPENUM: ',info['SHAPENUM'],
#	print '\t',shape

for info, shape in zip(map.ZoningDistrict_test_2_info, map.ZoningDistrict_test_2):
	# print info
	zone = info['ZONECLASS']
	# print shape
	if zone == 'OVERLAY': 
		continue
	elif info['RINGNUM']>1:
		continue
	zone = zone[0]
	if zone == 'R':
		color = 'y'
	elif zone == 'C':
		color = 'c'
	elif zone == 'M':
		color = 'darkmagenta'
	elif zone == 'O':
		color = 'ivory'
	elif zone == 'P':
		color = 'forestgreen'
	
	patches = [mplPolygon(np.array(shape), True)]
	pc = PatchCollection(patches)
	pc.set_alpha(.7)
	pc.set_facecolor(color)
	pc.set_zorder(2)
	pc.set_linewidth(.1)
	pc.set_edgecolor('k')
	ax.add_collection(pc)

#####################################################################
#				Add Roads shapefile to map 							#
#####################################################################
map.readshapefile('RoadCenterlines/RoadCenterlines_2',
	'RoadCenterlines_2', linewidth=.2)

#####################################################################
#						TRY CODE HERE 								#
#####################################################################



c = fiona.open('ZoningDistrict/ZoningDistrict_test_2.shp')

n = len(x_coordinates)
print 'the number of addresses is ',
print n

mult_arr = []
for x in c:
	print x
	if x['properties']['ZONECLASS']=='OVERLAY':
		continue
	tmp_arr = np.array(x['geometry']['coordinates']) 
	if tmp_arr.ndim == 1: 
		mult_arr.append(x['geometry']['coordinates'])
# count = 1
# for x in mult_arr:
# 	print '****************************************'
# 	print '*************** SHAPE ',count,' ***************'
# 	print '****************************************'
# 	for y in x:
# 		print y
# 		print '-------------------------------------'
# 	print '\n\n'
'''
count = 0
while count < n:
	poin = shapelyPoint(x_coordinates[count], y_coordinates[count])
	result = str(count) + '\t' + new_addresses[count] + '\t' + str(x_coordinates[count])+','+str(y_coordinates[count])+'\t'
	for x in c:
		if x['properties']['ZONECLASS']=='OVERLAY':
			continue
		tmp_arr = np.array(x['geometry']['coordinates']) 
		if tmp_arr.ndim == 1: 
			#Do stuff with multidimensional strings 
			continue
		poly = shapelyPolygon(x['geometry']['coordinates'])
		if poin.within(poly):
			result = result + x['properties']['ZONECLASS']
	print result
	count+=1
'''

	#print x['properties']['ZONECLASS'] + '\t'+ x['geometry']['type']+'\t'+  x['properties']['GlobalID']+'\t',
	#b = np.array(x['geometry']['coordinates'])
	#print b.ndim
	#print '\n---------------------------------------------------------\n---------------------------------------------------------\n'

'''
count = 0
for x in c:
	print x['properties']['ZONECLASS'] + '\n'
	p = Polygon(x['geometry']['coordinates'], True)
	print p
	print '\n---------------------------------------------------------\n---------------------------------------------------------\n'
	count+=1
'''

#####################################################################
#			 					END 								#
#####################################################################


x,y = map(x_coordinates, y_coordinates)
#
counter = 0
for a in new_addresses[:]:
	map.plot(x[counter], y[counter], 'bo', markersize=5, color='fuchsia')
	counter += 1 
print '.......................DONE!'
plt.show()