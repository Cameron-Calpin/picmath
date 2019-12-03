import xlrd, datetime

workbook = xlrd.open_workbook('Incidents by Offense 2016 to 2018 with coordinates and zones.xlsx')
worksheet = workbook.sheet_by_name('CPS Referral')
workbook_datemode = workbook.datemode

wrong_dates = []
for i in range(1, worksheet.nrows):
	# print worksheet.cell_value(i, 1)
	wrong_dates.append(float(worksheet.cell_value(i, 1)))

# wrong_dates_tuple = tuple(wrong_dates)
# print wrong_dates_tuple
January = []
February = [] 
March = []
April = []
May = []
June = []
July = []
August = []
September = []
October = []
November = []
December = []
for num in wrong_dates[1:]:
	# print num
	y, mo, d, h, mi, s = xlrd.xldate_as_tuple(num, workbook_datemode)
	# print "{0}/{1}/{2}".format(mo, d, y)

	if mo == 1:
		January.append(mo)
	elif mo == 2:
		February.append(mo)
	elif mo == 3:
		March.append(mo)
	elif mo == 4:
		April.append(mo)
	elif mo == 5:
		May.append(mo)
	elif mo == 6:
		June.append(mo)
	elif mo == 7:
		July.append(mo)
	elif mo == 8:
		August.append(mo)
	elif mo == 9:
		September.append(mo)
	elif mo == 10:
		October.append(mo)
	elif mo == 11:
		November.append(mo)
	else:
		December.append(mo)
	
print "January: ", len(January)
print "February: ", len(February)
print "March: ", len(March)
print "April: ", len(April)
print "May: ", len(May)
print "June: ", len(June)
print "July: ", len(July)
print "August: ", len(August)
print "September: ", len(September)
print "October: ", len(October)
print "November: ", len(November)
print "December: ", len(December)