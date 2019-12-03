########################################################################
####							Imports 							####
########################################################################
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from googlemaps import Client as GoogleMaps
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.collections import PatchCollection
import geopandas as gdp
import fiona
from shapely.geometry import Point as shapelyPoint
from shapely.geometry.polygon import Polygon as shapelyPolygon
import csv
import itertools
# import xlrd

#csvfile 	= 'Incidents 2016 to 2018.csv'
#data = pd.read_csv(csvfile)
########################################################################
####						Read Excel file 						####
########################################################################
# xlsxfile 	= 'Incidents by Offense 2016 to 2018.xlsx'
# #xlsxfile 	= 'Incidents 2016 to 2018 no dups.xlsx'
# # sheet		= 'Pocket Picking'
# # data = pd.read_excel(xlsxfile, sheet_name=sheet)
# data = pd.ExcelFile(xlsxfile)
# data_sheet_names = data.sheet_names
# # print len(data.sheet_names)

# for sheet in itertools.islice(data.sheet_names, 73, len(data.sheet_names)):
# 	# print sheet
# 	data = pd.read_excel(xlsxfile, sheet_name=sheet)

xlsxfile 	= 'Incidents by Offense 2016 to 2018 with coordinates and zones.xlsx'
data = pd.ExcelFile(xlsxfile)
data_sheet_names = data.sheet_names
# print(data_sheet_names)

# len(data.sheet_names)
for sheet in itertools.islice(data.sheet_names, 0, 1):
	sheet_file = sheet + '.csv'
	data = pd.read_excel(xlsxfile, sheet_name=sheet)

	violent_crimes		= []
	property_crimes 	= []


	a  = data['ADDRESS'].values
	r = data['REPORT NUMBER'].values
	d = data['DATE'].values
	t = data['TIME'].values
	o = data['OFFENSE'].values
	x = data['X_Coordinates'].values
	y = data['Y_Coordinates'].values


	########################################################################
	####				Initiate Google Maps Client 					####
	########################################################################
	# gmaps = GoogleMaps('AIzaSyDAQjEueKtHkby1KhCto7dD4GVnG4bPGTM')


	########################################################################
	####		Determine the (lat, lon) of each address 				####
	####		Modifies the addresses so they can be read by gmaps 	####
	####			places x coordinates in x_coordinates list 			####
	####			places y coordinates in y_coordinates list 			####
	####			places x coordinates in x_coordinates list 			####
	########################################################################
	# print '\nHERE ARE THE ADDRESSES:..............' 
	# #a = ['11800 BLK CANON BLVD','9TH ST / TAYLOR AVE']
	new_addresses = []
	address_nosfx = []
	x_coordinates = []
	y_coordinates = []
	address_zones = []
	date_array    = []
	time_array    = []
	offense_array = []
	repnum_array  = []

	count = 0
	for q in a[:]:

		if "BLK" in q:
			new_string = q.replace(" BLK", "")
		else:
			new_string = q
		# location = gmaps.geocode(new_string + ', Newport News, VA')
		# if(len(location)==0):
		# 	count+=1 
		# 	continue		
		new_addresses.append(new_string + ', Newport News, VA')
		address_nosfx.append(new_string)
		x_coordinates.append(x[count])
		y_coordinates.append(y[count])
		date_array.append(d[count])
		time_array.append(t[count])
		offense_array.append(o[count])
		repnum_array.append(r[count])

		# print count, x_coordinates[count]
		count+=1


	########################################################################
	####			Initiate Basemap in addition to subplots 			####
	########################################################################
	print '\nProcessing Map Image........\t'
	fig, ax = plt.subplots()
	# (-76.62686736643403, 36.960797041307146, -76.3876260594103, 37.22066807617356)
	map = Basemap(projection='merc', lat_0 = 36.9786449, lon_0 = -76.4321089,
	    resolution ='h', area_thresh = 0.1,
	    llcrnrlon=-76.62686736643403, llcrnrlat=36.96079704130714,
	    urcrnrlon=-76.3876260594103, urcrnrlat=37.22066807617356)
	map.drawcoastlines()
	map.drawcountries()
	map.drawmapboundary(fill_color='aqua')
	map.fillcontinents(color = 'dimgrey',lake_color='aqua')
	patches = []

	########################################################################
	####				Add Zones shapefile to map 			 			####
	########################################################################
	map.readshapefile('ZoningDistrict/ZoningDistrict_test_2', 
		'ZoningDistrict_test_2', drawbounds = False)


	########################################################################
	####				Add Roads shapefile to map 			 			####
	########################################################################
	map.readshapefile('RoadCenterlines/RoadCenterlines_2',
		'RoadCenterlines_2', linewidth=.2)

	########################################################################
	####						TRY CODE HERE 							####
	########################################################################
	c = fiona.open('ZoningDistrict/ZoningDistrict_test_2.shp')


	########################################################################
	####				ls 	= LineString list 	 			 			####
	####				mls = MultiLineString list
	####				pnts = List of points
	########################################################################
	ls 		= []
	lsz		= []
	mls 	= []
	mlsz	= []
	pnts 	= []


	for x in c:
		coords = x['geometry']['coordinates']
		if x['properties']['ZONECLASS'] == 'OVERLAY':
			continue
		tmp = np.array(coords)
		if tmp.ndim == 1: # Shape is a MultiLineString
			poly = shapelyPolygon(coords[0])
			mls.append(poly)
			mlsz.append(x['properties']['ZONECLASS'])
		elif tmp.ndim == 2: # Shape is a LineString
			poly = shapelyPolygon(coords)
			ls.append(poly)
			lsz.append(x['properties']['ZONECLASS'])



	n = len(x_coordinates)
	i = 0
	while i < n:
		pnts.append(shapelyPoint(x_coordinates[i], y_coordinates[i]))
		i+=1


	output_file = open('output.csv', mode='w')
	out_write = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	# Store zones
	zones = []

	c_res,c_ofc,c_prk,c_ind,c_com,c_nzn = 0,0,0,0,0,0
	n = len(pnts) #something
	i = 0
	while i < n:
		p = pnts[i]
		found = False
		k = -1
		for x in ls:
			k+=1
			if p.within(x):
				found = True
				#print p,'\t',lsz[k]
				# print repnum_array[i],'\t',date_array[i],'\t',time_array[i],'\t',offense_array[i],'\t',lsz[k],'\t',address_nosfx[i]
				out_write.writerow([repnum_array[i],date_array[i],time_array[i],offense_array[i],lsz[k],address_nosfx[i]])
				t = lsz[k][0]
				zones.append(t)
				if t=='R': c_res+=1
				elif t=='O': c_ofc+=1
				elif t=='P': c_prk+=1
				elif t=='C': c_com+=1
				elif t=='M': c_ind+=1
				break
		if found==False:
			k=-1
			for x in mls:
				k+=1
				if p.within(x):
					found = True
					#print p,'\t',mlsz[k]
					# print repnum_array[i],'\t',date_array[i],'\t',time_array[i],'\t',offense_array[i],'\t',mlsz[k],'\t',address_nosfx[i]
					out_write.writerow([repnum_array[i],date_array[i],time_array[i],offense_array[i],mlsz[k],address_nosfx[i]])
					t = mlsz[k][0]
					zones.append(t)
					if t=='R': c_res+=1
					elif t=='O': c_ofc+=1
					elif t=='P': c_prk+=1
					elif t=='C': c_com+=1
					elif t=='M': c_ind+=1
					break

		if found == False:
			#print p, '\t', 'NO ZONE'
			zones.append('NZ')
			# print repnum_array[i],'\t',date_array[i],'\t',time_array[i],'\t',offense_array[i],'\t','NZ','\t',address_nosfx[i]
			out_write.writerow([repnum_array[i],date_array[i],time_array[i],offense_array[i],'NZ',address_nosfx[i]])

			c_nzn+=1
		i+=1
	output_file.close()
	total = c_res+c_ofc+c_prk+c_ind+c_com+c_nzn

	# for i in range(len(zones)):
	# 	print zones[i]

	####################################################################
	# 						Output to Excel Sheet				   	   #											
	####################################################################
	# workbook = xlrd.open_workbook('Incidents by Offense 2016 to 2018.xlsx')
	# worksheet = workbook.sheet_by_name('Pocket Picking')
	# workbook_datemode = workbook.datemode

	# x_coordinates_col = []
	# y_coordinates_col = []
	# zones_col = []

	# for i in range(len(x_coordinates)):
	# 	x_coordinates_col.append([x_coordinates[i]])
	# np_x_coordinates_col = np.array(x_coordinates_col)
	# # print np_x_coordinates_col

	# for i in range(len(y_coordinates)):
	# 	y_coordinates_col.append([y_coordinates[i]])
	# np_y_coordinates_col = np.array(y_coordinates_col)
	# # print np_y_coordinates_col

	# for i in range(len(zones)):
	# 	zones_col.append([zones[i]])
	# np_zones_col = np.array(zones_col)
	# # print np_zones_col

	# pd_data_col = pd.DataFrame({'X_Coordinates':np_x_coordinates_col[:,0], 'Y_Coordinates':np_y_coordinates_col[:,0], 'Zones':np_zones_col[:,0]})
	# # pd_y_coordinates_col = pd.DataFrame({'Y_Coordinates':np_y_coordinates_col[:,0]})
	# print pd_data_col
	# # print pd_y_coordinates_col

	# to_update = {sheet : pd_data_col}

	# # load existing data
	# excel_reader = pd.ExcelFile(xlsxfile)

	# # write and update
	# excel_writer = pd.ExcelWriter(xlsxfile)

	# for sheet in excel_reader.sheet_names:
	# 	sheet_df = excel_reader.parse(sheet)
	# 	append_df =  to_update.get(sheet)

	# 	if append_df is not None:
	# 		sheet_df = pd.concat([sheet_df, append_df], axis=1)

	# 	sheet_df.to_excel(excel_writer, sheet, index=False)
	# excel_writer.save()

	####################################################################

	# map_df = gdp.read_file("ZoningDistrict/ZoningDistrict_test_2.shp")
	# map_df.head()
	# map_df.plot()

	for info, shape in zip(map.ZoningDistrict_test_2_info, map.ZoningDistrict_test_2):
		zone = info['ZONECLASS']
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
			color = 'purple'
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
	#			 					END 								#
	#####################################################################


	# x,y = map(x_coordinates, y_coordinates)
	# #
	# counter = 0
	# for a in new_addresses[:]:
	# 	map.plot(x[counter], y[counter], 'bo', markersize=5, color='fuchsia')
	# 	counter += 1 
	# print '.......................DONE!'
	# plt.show()
	continue
