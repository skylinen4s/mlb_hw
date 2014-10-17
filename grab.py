import httplib
import urllib2
import re
import sys

def debug_print(s ,msg = None):
	print "DEBUG", msg, s
	pass

def get_site1(year = 2014, month = 8, day = 30, start = 0, num = 30):
	return 'https://www.google.com/finance/historical?q=INDEXDJX:.DJI' + \
           '&startdate=' + str(month) + '/' + str(day) + '/' + str(year) + \
           '&start=' + str(start) + '&num=' + str(num)

#command: python grab.py 2014 01 01 2014 09 10
def get_site2(start_year = 2014, start_month = 8, start_day = 30, end_year = 2014, end_month = 10, end_day = 10):
	return 'https://www.google.com/finance/historical?q=INDEXDJX:.DJI' + \
           '&startdate=' + str(start_month) + '/' + str(start_day) + '/' + str(start_year) + \
           '&enddate=' + str(end_month) + '/' + str(end_day) + '/' + str(end_year)
#test
#debug_print(get_site(1, 31, 2012, 0, 40))
#debug_print(get_site())

#target 
pattern = r'<td class="lm">(.+)' + \
           '\s<td class="rgt">([\d\,\.]+)' + \
           '\s<td class="rgt">([\d\,\.]+)' + \
           '\s<td class="rgt">([\d\,\.]+)' + \
           '\s<td class="rgt">([\d\,\.]+)' + \
           '\s<td class="rgt rm">([\d\,\,]+)'
reg_price = re.compile(pattern)

pattern_total_size = r'google\.finance\.applyPagination\(\s+\d+,\s+\d+,\s+(\d+),\s+'
reg_row_size =  re.compile(pattern_total_size)

def get_data(fileName):
	f = open(fileName, 'a')
	## Get web page content
	if len(sys.argv) == 1:
		print "defult!\nfetch date from '2014.08.30' to '2014.10.10'"
		start_date = [2014, 8, 30]
		end_date = [2014, 10, 10]
	elif len(sys.argv) == 7:
		start_date = [sys.argv[1],sys.argv[2],sys.argv[3]]
		end_date = [sys.argv[4],sys.argv[5],sys.argv[6]]
		print "fetch data from " + start_date[0] + '.' + start_date[1] + '.' + start_date[2] + ' to ' +\
								   end_date[0] + '.' + end_date[1] + '.' + end_date[2]
	else:
		print "Wrong date form"
		return 0

	urlsite = get_site2(start_date[0], start_date[1], start_date[2], end_date[0], end_date[1], end_date[2])
	content = opener.open(urlsite).read()

	match_r_sz = reg_row_size.search(content)

	## size
	row_size = int(match_r_sz.groups()[0])
	print "data size: " + str(row_size)

	## page number, 30row/page
	page_number = row_size/30 + 1;
	print "pages: " + str(page_number)
	page_range = range(page_number)

	## fetch data
	f.write("year-month-date,volume,open,high,low,close\n")
	check_size = 0
	for i in page_range:
		print "fetching data : " + str(i+1) + "/" + str(page_number)
		#show rows defult setting of website: 30 rows 
		start_pos = i*30
		site = get_site1(start_date[0], start_date[1], start_date[2], start_pos, 30)

		cnt = opener.open(site).read()
		stock_data = reg_price.findall(cnt)
		length = len(stock_data)
		if(length is 0):
			print "stock data not found"
			return None
		else:
			for i in range(length):
				#f.write(str(stock_data[i]))
				check_size += 1
				stock_date = transform(stock_data[i][0])
				stock_open = ch_remove(stock_data[i][1], ',')
				stock_high = ch_remove(stock_data[i][2], ',')
				stock_low = ch_remove(stock_data[i][3], ',')
				stock_close = ch_remove(stock_data[i][4], ',')
				stock_volume = ch_remove(stock_data[i][5], ',')

				f.write(str(stock_date) + ',' + \
				 		str(stock_volume) + ',' + \
				 		str(stock_open) + ',' + \
				 		str(stock_high) + ',' + \
				 		str(stock_low) + ',' + \
				 		str(stock_close))
				f.write("\n")
	print "data fetched: ",check_size
	if(check_size == row_size):
		print "data check!"
## transform the format fo time
def transform(date):
	date = date.split(' ')
	## original : month day year
	## target   : year-montg-day

	## month
	if   (date[0] == 'Jan') : date[0] = '01'
	elif (date[0] == 'Feb') : date[0] = '02'
	elif (date[0] == 'Mar') : date[0] = '03'
	elif (date[0] == 'Apr') : date[0] = '04'
	elif (date[0] == 'May') : date[0] = '05'
	elif (date[0] == 'Jun') : date[0] = '06'
	elif (date[0] == 'Jul') : date[0] = '07'
	elif (date[0] == 'Aug') : date[0] = '08'
	elif (date[0] == 'Sep') : date[0] = '09'
	elif (date[0] == 'Oct') : date[0] = '10'
	elif (date[0] == 'Nov') : date[0] = '11'
	elif (date[0] == 'Dec') : date[0] = '12'

	## day
	#date[1] = date[1].center(3, '0').split(',')[0]
	date[1] = date[1].zfill(3).split(',')[0]
	## target   : year-montg-day
	return date[2] + '-' + date[0] + '-' + date[1]

## remove a character from a string 
def ch_remove(tmp_str, char):
	tmp_str = tmp_str.split(char)
	string = ''
	for i in range(len(tmp_str)):
		string += tmp_str[i]
	return string

# Open File
fileName = 'test.txt'
f = open(fileName, 'w')
f.close()
httplib.HTTPConnection.debuglevel = 1
opener = urllib2.build_opener()


print '--- Start fetch ---'
get_data(fileName)
print '--- End fetch ---'