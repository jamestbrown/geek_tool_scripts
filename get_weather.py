#! /usr/bin/python
# James Thomas Brown
# get_weather program that obtains the weather for two days
# based on your location

import urllib2
import string
import datetime

#ZIP = 00000

def temp_convert(fah):
	cel = (fah-32) * 5/9
	return str(fah)+" F ("+ str(cel) + " C)"


def find_zip():
	city_info_web = 'http://www.komar.org/cgi-bin/ip_to_country.pl'
	req = urllib2.Request(city_info_web)
	rdata = urllib2.urlopen(req)
	city_info = rdata.read()
	
	lat_start = city_info.find("Your City Latitude")
	city_lat = city_info[lat_start:lat_start+39]
	city_lat_sign = ' ' + city_lat[-1]
	city_lat = city_lat[26:33]
	
	long_start = city_info.find("Your City Longitude     : ")
	city_long = city_info[long_start:long_start+39]
	city_long_sign = ' ' + city_long[-1]
	city_long = city_long[26:33]
	
	zip_start = city_info.find("Your City Postal Code   : ")
	city_zip = city_info[zip_start:zip_start+31][26:]
	
	return city_zip, str(city_lat) + city_lat_sign, str(city_long) + city_long_sign
 

def find_forecast(ZIP, geo_lat, geo_long):
	weather_url = 'http://www.google.com/ig/api?weather=' + str(ZIP)
	req = urllib2.Request(weather_url)
	xml_weather_data = urllib2.urlopen(req)
	xml_weather = xml_weather_data.read()
	xml_weather = xml_weather.split('><')[4:35]
	
	city = ''
	current_temp = ''
	current_cond = ''
	lows = '  Lows  \t\t||'
	highs ='  Highs \t\t||' 
	
	for line in xml_weather:
		if line[0:6] == "temp_f":
			current_temp = current_temp + temp_convert(int(line[13:-2]))
			#current_temp = current_temp + line[13:-2] + " F"
		elif line[0:11] == "city data=\"":
			city = line[11:-2]
		elif line[0:10] == "low data=\"":
			#lows = lows + "\t" + line[10:-2] + " F" + "\t||"
			lows = lows + temp_convert(int(line[10:-2])) + " \t||"
		elif line[0:16] == "condition data=\"":
			# current conditions displayed
			#current_cond = current_cond + line[16:-2]
			if len(line[16:-2]) > 8:
				current_cond = current_cond + line[16:-2] + " \t||"
			else:
				current_cond = current_cond + line[16:-2] +" \t\t||"
		elif line[0:11] == "high data=\"":
			#highs = highs + "\t" + line[11:-2] + " F" + "\t||"
			highs = highs + temp_convert(int(line[11:-2])) + " \t||"
			
	#print "\n"
	print "Geo-Coorinates: " + geo_lat + ", "+ geo_long
	print "Current City:  " + city + " -- Current Temp " + current_temp
	print "Now \t\t\t|| Today \t\t|| Tomorrow \t||"
	print current_cond
	print highs
	print lows



def main():
	global ZIP
	geo_lat = ''
	geo_lat = ''
	
	ZIP, geo_lat, geo_long = find_zip()
	#print ZIP
	#print geo_lat
	#print geo_long
	find_forecast(ZIP, geo_lat, geo_long)
	now = datetime.datetime.now()
	print "The last update was on: " + now.strftime("%m-%d at %H:%M")
	
	


if __name__ == "__main__":
	main()