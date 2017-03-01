#!/usr/bin/python
import os

def extract():
	for x in xrange(1,1001):
		print str(x)
		string = "curl -X GET --header \"Accept: application/json\" --header \"user-key: 3664838525f7d1b0ba37aaf409c79501\" \"https://developers.zomato.com/api/v2.1/restaurant?res_id=" + str(x) + "\" > " + str(x) + "out.json"
		print string
		os.system(string)

if __name__ == '__main__':
	extract()