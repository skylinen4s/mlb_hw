import sys
import glob
import os

startday = sys.argv[1]+'-'+sys.argv[2]+'-'+sys.argv[3]
endday = sys.argv[4]+'-'+sys.argv[5]+'-'+sys.argv[6]

print "start: ",startday
print "end: ",endday

outputFile = 'train_data.txt'
out = open(outputFile, 'w')

def getData(fileName):
	data = fileName.readline().rstrip('\n').split(',')
	if len(data) is 1:
		for i in range(7):
			data.insert(i,'0')
		data.remove('')
	for i in range(len(data)):
		if data[i] == "NULL":
			data[i] = "0"
	return data

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

		if data0[0] == endday:
			end = True
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

		if data3[0] == startday or data3[0] == '0':
			break

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
		print train_data
		
	f.close()
out.close()