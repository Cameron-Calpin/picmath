########################################################################
####							Imports 							####
########################################################################
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from matplotlib.patches import Polygon as mplPolygon
from matplotlib.collections import PatchCollection
import geopandas as gdp
import fiona
from shapely.geometry import Point as shapelyPoint
from shapely.geometry.polygon import Polygon as shapelyPolygon
import csv
import sys

crime_sheets = ['Deceased Person','Disorderly Conduct','Driving Under the Influence','Drug Equipment- Possess',
'DrugNarcotics Offenses','Drunkenness',	'Embezzle',	'Extort','Family Offenses, Nonviolent',
'Forcible Fondling','Forcible Sodomy','ForgeryCounterfeiting','Fraud - Impersonate',
'Fraud - Welfare','Fraud By Wire','Fraud-Illegal Use Credit CardAT','Fraud-Illegal Use of Credit Car',
'FraudFalse PretensesSwindle','Gambling-BettingWagering','Habitual Traffic Offender','Hit and Run',
'HomicideMurder','Incest With Minor','Indecent Exposure','Intimidation','Justifiable Homicide',
'Juvenile - Runaway','KidnapAbduction','Larceny','Leaving the Scene','Liquor Law Violations','Loitering',
'Missing Person','Neglect Child','Obscene MaterialPornography','Overdose','Peeping Tom','Pocket Picking',
'Prostitution',	'Purse Snatching - No Force','Robbery','Sex Assault, Rape','Sexual Assault w an Object',
'Shoplifting','Simple Assault','Statutory Rape','Stolen Property','Suicide','Tampering With Auto',
'Theft From Building','Theft From Coin Operated Machin','Theft From Vehicle','Theft Parts From Vehicle',
'Tobacco Violation','Traffic Fatality','Trespassing','Truancy - Regular Patrol','Unauthorized Use of Vehicle',
'VEH Recovery (Out of Juris)','Vehicle Theft','Weapon Offense']

#csvfile 	= 'Incidents 2016 to 2018.csv'
#data = pd.read_csv(csvfile)
########################################################################
####						Read Excel file 						####
########################################################################
xlsxfile 	= 'Incidents by Offense 2016 to 2018 with coordinates and zones.xlsx'
#xlsxfile 	= 'Incidents 2016 to 2018 no dups.xlsx'



sheet_file = 'Sexual Assault'
data = pd.read_excel(xlsxfile, sheet_name=sheet_file)

#data = pd.read_excel(xlsxfile)

violent_crimes		= []
property_crimes 	= []


a = data['ADDRESS'].values
r = data['REPORT NUMBER'].values
d = data['DATE'].values
t = data['TIME'].values
o = data['OFFENSE'].values
x = data['X_Coordinates'].values
y = data['Y_Coordinates'].values

########################################################################
####				Initiate Google Maps Client 					####
########################################################################
# gmaps = GoogleMaps('AIzaSyA2n2IG7CoVi3CVbCwXfojiqTJtEWDMeMo')


########################################################################
####		Determine the (lat, lon) of each address 				####
####		Modifies the addresses so they can be read by gmaps 	####
####			places x coordinates in x_coordinates list 			####
####			places y coordinates in y_coordinates list 			####
####			places x coordinates in x_coordinates list 			####
########################################################################
# print '\nHERE ARE THE ADDRESSES:..............' 
#a = ['11800 BLK CANON BLVD','9TH ST / TAYLOR AVE']
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
# print len(a)
# print len(x)
for a in a[:]:

	if "BLK" in x:
		new_string = a.replace(" BLK", "")
	else:
		new_string = a
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

	# print count,'\t', new_string, '\t',x_coordinates[count], '\t', y_coordinates[count]
	count+=1


########################################################################
####			Initiate Basemap in addition to subplots 			####
########################################################################
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

c_res_1, c_res_2, c_res_3, c_res_4, c_res_5, c_res_6, c_res_7, c_res_8, c_res_9 = 0,0,0,0,0,0,0,0,0
c_ofc_1, c_ofc_2, c_ofc_3 = 0,0,0
c_prk_1 = 0
c_ind_1, c_ind_2 = 0,0
c_com_1, c_com_2, c_com_3, c_com_4, c_com_5 = 0,0,0,0,0 
c_nzn = 0
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
			t = lsz[k]
			# print lsz[k]
			if t=='R1': c_res_1+=1
			elif t=='R2': c_res_2+=1
			elif t=='R3': c_res_3+=1
			elif t=='R4': c_res_4+=1
			elif t=='R5': c_res_5+=1
			elif t=='R6': c_res_6+=1
			elif t=='R7': c_res_7+=1
			elif t=='R8': c_res_8+=1
			elif t=='R9': c_res_9+=1
			elif t=='O1': c_ofc_1+=1
			elif t=='O2': c_ofc_2+=1
			elif t=='O3': c_ofc_3+=1 
			elif t=='P1': c_prk_1+=1
			elif t=='C1': c_com_1+=1
			elif t=='C2': c_com_2+=1
			elif t=='C3': c_com_3+=1
			elif t=='C4': c_com_4+=1
			elif t=='C5': c_com_5+=1
			elif t=='M1': c_ind_1+=1
			elif t=='M2': c_ind_2+=1
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
				t = mlsz[k]
				if t=='R1': c_res_1+=1
				elif t=='R2': c_res_2+=1
				elif t=='R3': c_res_3+=1
				elif t=='R4': c_res_4+=1
				elif t=='R5': c_res_5+=1
				elif t=='R6': c_res_6+=1
				elif t=='R7': c_res_7+=1
				elif t=='R8': c_res_8+=1
				elif t=='R9': c_res_9+=1
				elif t=='O1': c_ofc_1+=1
				elif t=='O2': c_ofc_2+=1
				elif t=='O3': c_ofc_3+=1 
				elif t=='P1': c_prk_1+=1
				elif t=='C1': c_com_1+=1
				elif t=='C2': c_com_2+=1
				elif t=='C3': c_com_3+=1
				elif t=='C4': c_com_4+=1
				elif t=='C5': c_com_5+=1
				elif t=='M1': c_ind_1+=1
				elif t=='M2': c_ind_2+=1
				break

	if found == False:
		#print p, '\t', 'NO ZONE'
		# print repnum_array[i],'\t',date_array[i],'\t',time_array[i],'\t',offense_array[i],'\t','NZ','\t',address_nosfx[i]
		out_write.writerow([repnum_array[i],date_array[i],time_array[i],offense_array[i],'NZ',address_nosfx[i]])

		c_nzn+=1
	i+=1
output_file.close()
total = c_res_1+c_res_2+c_res_3+c_res_4+c_res_5+c_res_6+c_res_7+c_res_8+c_res_9+c_ofc_1+c_ofc_2+c_ofc_3+c_prk_1+c_ind_1+c_ind_2+c_com_1+c_com_2+c_com_3+c_com_4+c_com_5+c_nzn

def percent(num):
	g = int(float(num)/float(total)*1000.0)
	return g*.1

print 'Residential 1: ','\t',c_res_1,'\t',percent(c_res_1)
print 'Residential 2: ','\t',c_res_2,'\t',percent(c_res_2)
print 'Residential 3: ','\t',c_res_3,'\t',percent(c_res_3)
print 'Residential 4: ','\t',c_res_4,'\t',percent(c_res_4)
print 'Residential 5: ','\t',c_res_5,'\t',percent(c_res_5)
print 'Residential 6: ','\t',c_res_6,'\t',percent(c_res_6)
print 'Residential 7: ','\t',c_res_7,'\t',percent(c_res_7)
print 'Residential 8: ','\t',c_res_8,'\t',percent(c_res_8)
print 'Residential 9: ','\t',c_res_9,'\t',percent(c_res_9)
print 'Office 1: ','\t\t\t',c_ofc_1,'\t',percent(c_ofc_1)
print 'Office 2: ','\t\t\t',c_ofc_2,'\t',percent(c_ofc_2)
print 'Office 3: ','\t\t\t',c_ofc_3,'\t',percent(c_ofc_3)
print 'Park 1: ','\t\t\t',c_prk_1,'\t',percent(c_prk_1)
print 'Industrial 1: ','\t\t',c_ind_1,'\t',percent(c_ind_1)
print 'Industrial 2: ','\t\t',c_ind_2,'\t',percent(c_ind_2)
print 'Commercial 1: ','\t\t',c_com_1,'\t',percent(c_com_1)
print 'Commercial 2: ','\t\t',c_com_2,'\t',percent(c_com_2)
print 'Commercial 3: ','\t\t',c_com_3,'\t',percent(c_com_3)
print 'No Zone: ','\t\t\t',c_nzn,'\t',percent(c_nzn)
# print '\t\t\t', int(percent(c_res)+percent(c_ofc)+percent(c_prk)+percent(c_ind)+percent(c_com)+percent(c_nzn))


def get_color(zone, percentage):
	percent_boi = percent(percentage)
	# print "Percent Boi: ", percent_boi
	# print "Zone Boi: ", zone
	if percent_boi <= 4.4:
		color = '#00FF00'
		return color
	elif percent_boi > 4.4 and percent_boi <= 8.8:
		color = '#80FF00'
		return color
	elif percent_boi > 8.8 and percent_boi <= 13.2:
		color = '#FFFF00'
		return color
	elif percent_boi > 13.5 and percent_boi <= 18:
		color = '#FF8000'
		return color
	elif percent_boi > 18 and percent_boi <= 22.6:
		color = '#FF0000'
		return color



########################################################################
####  				Add colors to each zone 						####	
####  																####
#### 	https://matplotlib.org/examples/color/named_colors.html		####
####  	ZONECLASS 	== R1, R2, R3, R4, R5, R6, R7, R8, R9			####
#### 			 	== C1, C2, C3, C4, C5, O1, O2, O3				####
####			 	== M1, M2, M3, P1, OVERLAY						####
####  	This for loop defines the colors of each zone 				####
########################################################################
zune = []
for info, shape in zip(map.ZoningDistrict_test_2_info, map.ZoningDistrict_test_2):
	zone = info['ZONECLASS']
	# print zone
	if zone == 'OVERLAY': 
		continue
	elif info['RINGNUM']>1:
		continue
	# zone = zone[0]
	if zone == 'C1':
		# color = '#33FF33'
		color = get_color(zone, c_com_1)
	elif zone == 'C2':
		color = get_color(zone, c_com_2)
	elif zone == 'C3':
		color = get_color(zone, c_com_3)
	elif zone == 'C4':
		color = get_color(zone, c_com_4)
	elif zone == 'C5':
		color = get_color(zone, c_com_5)
	elif zone == 'M1':
		color = get_color(zone, c_ind_1)
	elif zone == 'M2':
		color = get_color(zone, c_ind_2)
	elif zone == 'O1':
		color = get_color(zone, c_ofc_1)
	elif zone == 'O2':
		color = get_color(zone, c_ofc_2)
	elif zone == 'O3':
		color = get_color(zone, c_ofc_3)
	elif zone == 'P1':
		color = get_color(zone, c_prk_1)
	elif zone == 'R1':
		color = get_color(zone, c_res_1)
	elif zone == 'R2':
		color = get_color(zone, c_res_2)
	elif zone == 'R3':
		color = get_color(zone, c_res_3)
	elif zone == 'R4':
		color = get_color(zone, c_res_4)
	elif zone == 'R5':
		color = get_color(zone, c_res_5)
	elif zone == 'R6':
		color = get_color(zone, c_res_6)
	elif zone == 'R7':
		color = get_color(zone, c_res_7)
	elif zone == 'R8':
		color = get_color(zone, c_res_8)
	elif zone == 'R9':
		color = get_color(zone, c_res_9)
	else:
		continue

	
	zune.append(zone)
	patches = [mplPolygon(np.array(shape), True)]
	pc = PatchCollection(patches)
	pc.set_alpha(.7)
	pc.set_facecolor(color)
	pc.set_zorder(2)
	pc.set_linewidth(.1)
	pc.set_edgecolor('k')
	ax.add_collection(pc)


def Remove(duplicate): 
	final_list = [] 
	for num in duplicate: 
		if num not in final_list: 
			final_list.append(num) 
	return final_list 

def sorted_nicely( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

new_zone = Remove(zune)
# print zune
new_zone = sorted_nicely(new_zone)
# print new_zone
#####################################################################
#			 					END 								#
#####################################################################


x,y = map(x_coordinates, y_coordinates)
#
# counter = 0
# for a in new_addresses[:]:
# 	map.plot(x[counter], y[counter], 'bo', markersize=5, color='fuchsia')
# 	counter += 1 
# print '.......................DONE!'
plt.show()
