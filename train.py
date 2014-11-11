import sys
import glob
import os
import datetime

def tranDate(date):
	if date is not '0':
		date = date.split('-')
		date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
		return date
	else:
		return 0

def getData(fileName):
	data = fileName.readline().rstrip('\n').split(',')
	if len(data) is 1:
		for i in range(7):
			data.insert(i,'0')
		data.remove('')
	for i in range(len(data)):
		if data[i] == "NULL" or data[i] == "--":
			data[i] = "0"
	return data

sday = datetime.date(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
eday = datetime.date(int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))

print "Date1(start): ",sday
print "Date2(end): ",eday

if (sday.weekday() is 5) or (sday.weekday() is 6):
	print "Date1 is not weekday"
if (eday.weekday() is 5) or (eday.weekday() is 6):
	print "Date2 is not weekday"

outputFile = 'train_data'
out = open(outputFile, 'w')

filenum = 0
for files in glob.glob('../stock/*'):
	filenum += 1
	inputFile = files
	f = open(inputFile, 'r')
	stockName = os.path.basename(inputFile)
	print "stock:"+str(stockName)+" number:"+str(filenum)
	#out.write(stockName+":")

	end = False
	while True:
		line = f.readline().rstrip('\n')
		if not line: break
		
		data0 = getData(f)
		d = tranDate(data0[0])
		if d == eday:
			end = True
			break
		if d < eday:
			print "There is no data of this day:", eday
			break
		if d < sday:
			print "There is no data of this day:", sday
			break

	num = 0
	while end:
		if num == 0:
			data1 = data0
			data2 = getData(f)
			data3 = getData(f)
		else:
			data1 = data2
			data2 = data3
			data3 = getData(f)

		num += 1

		if data2[4] is not "0":
			rise = (float(data1[4])-float(data2[4]))/float(data2[4])
		else:
			rise = 0

		if rise > 0.02:
			rise = 2
		elif rise > 0:
			rise = 1
		elif rise == 0 or rise == None:
			rise = 0
		elif rise > -0.02:
			rise = -1
		elif rise < -0.02:
			rise = -2

		if data3[4] is not "0":
			dif_rise = rise - ((float(data2[4])-float(data3[4]))/float(data3[4]))
		else:	
			dif_rise = rise - 0
		c_dif_rise = str(dif_rise)

		if data3[0] == '0':
			break

		if tranDate(data1[0]) == sday or tranDate(data1[0]) ==eday: 
			train_data = str(rise) + \
					  "\t1:"+data1[1]+ \
					  "\t2:"+data1[2]+ \
					  "\t3:"+data1[3]+ \
					  "\t4:"+data1[4]+ \
					  "\t5:"+data1[5]+ \
			          "\t6:"+data1[6]+ \
					  "\t7:"+data2[1]+ \
					  "\t8:"+data2[2]+ \
					  "\t9:"+data2[3]+ \
					  "\t10:"+data2[4]+ \
					  "\t11:"+data2[5]+ \
			          "\t12:"+data2[6]+ \
					  "\t13:"+data3[1]+ \
					  "\t14:"+data3[2]+ \
					  "\t15:"+data3[3]+ \
					  "\t16:"+data3[4]+ \
					  "\t17:"+data3[5]+ \
			          "\t18:"+data3[6]+ \
					  "\t19:"+c_dif_rise+"\n"
			out.write(train_data)
			#print train_data
			if tranDate(data1[0]) == sday:
				break
		
	f.close()
out.close()
