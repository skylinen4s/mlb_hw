import sys

startday = sys.argv[1]+'-'+sys.argv[2]+'-'+sys.argv[3]
endday = sys.argv[4]+'-'+sys.argv[5]+'-'+sys.argv[6]

print "start: ",startday
print "end: ",endday

inputFile = '../stock/2330'
f = open(inputFile, 'r')
outputFile = 'train_data.txt'
out = open(outputFile, 'w')

end = False
while True:
	line = f.readline().rstrip('\n')
	if not line: break

    data = line.split(',')
	if data[0] == endday:
		end = True
		break
num = 0
while end:
	if num == 0:
		data1 = data
		data2 = f.readline().rstrip('\n').split(',')
		data3 = f.readline().rstrip('\n').split(',')
	else:
		data1 = data2
		data2 = data3
		data3 = f.readline().rstrip('\n').split(',')
	num += 1

	rise = 0
	rise = (float(data1[4])-float(data2[4]))/float(data2[4])
	if rise >= 0.02:
		rise = 2
	elif rise > 0:
		rise = 1
	elif rise == 0 or rise == None:
		rise = 0
	elif rise > -0.02:
		rise = -1
	elif rise <= -0.02:
		rise = -2

	dif_rise = rise - ((float(data2[4])-float(data3[4]))/float(data3[4]))

	out.write(str(rise)+
			  "\t1:"+data1[1]+
			  "\t2:"+data1[2]+
			  "\t3:"+data1[3]+
			  "\t4:"+data1[4]+
			  "\t5:"+data1[5]+
              "\t6:"+data1[6]+
			  "\t7:"+data2[1]+
			  "\t8:"+data2[2]+
			  "\t9:"+data2[3]+
			  "\t10:"+data2[4]+
			  "\t11:"+data2[5]+
              "\t12:"+data2[6]+
			  "\t13:"+data3[1]+
			  "\t14:"+data3[2]+
			  "\t15:"+data3[3]+
			  "\t16:"+data3[4]+
			  "\t17:"+data3[5]+
              "\t18:"+data3[6]+
			  "\t19:"+str(dif_rise)+"\n")

	if data3[0] == startday or data3 == '':
		print "data size: ",num
		break

out.close()
f.close()


