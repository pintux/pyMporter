'''
The MIT License (MIT)

Copyright (c) <2013> <Antonio Pintus>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import csv
import argparse
import pymongo
from dateutil.parser import *
import datetime

def connect_to_db(dbname, collection):		
	#open mongoDB connection
	c = pymongo.MongoClient()
	db = c[dbname]
	coll = db[collection]
	return coll

def save_to_db(doc, collection):
	collection.save(doc)





def to_type(s,type):
	try:
		if type == "integer":
			return int(s)
		elif type == "float":
			return float(s)
		elif type == "date":
			return parse(s)
		elif type == "string":
			return unicode(s,'utf-8')

	except:
		return unicode(s,'utf-8')
		



def parse_headers(headers):
	if headers == None:
		headers_row = []
		print "- using first csv row as headers"
	else:
		headers_row = [[h.split(':')[0],h.split(':')[1]] if h.find(':')>-1 else [h,"string"] for h in headers.split(',')]
		print "- using headers:",str(headers_row)
	return headers_row


def import_csv(dbname, collection, headers, csv_file):
	rownum = 0	
	headers_row = parse_headers(headers)

	print "\nImporting CSV file to db: %s, collection: %s" % (dbname,collection)
	print "Start time:", datetime.datetime.now()
	try:

		coll = connect_to_db(dbname, collection)
		
		with open(csv_file, 'rb') as f:
		    reader = csv.reader(f)
		    for row in reader:
		    	if rownum == 0 and headers_row == []:
        			headers_row = [[h,"string"] for h in row]
        			rownum+=1
        			print "headers are: ", str(headers_row)
		        else:
		        	#prepare document and save to db
		        	doc = {}
		        	for i in range(0,len(headers_row)):
		        		doc[headers_row[i][0]] = to_type(row[i], headers_row[i][1])
		        	save_to_db(doc, coll)
		    print "...done."
		    print "End time:", datetime.datetime.now()



	except Exception as e:
		print "An error occurred:",e



if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='pyMporter: a minimalist tool to import a CSV file to MongoDB supporting headers types specification.')
	
	parser.add_argument("csv_file")
	parser.add_argument('--dbname', default='NewDB',
	                   help='MongoDB database name to use, default is NewDB')
	parser.add_argument('--collection', default='fromCSV',
	                   help='MongoDB collection name to import data to')
	parser.add_argument('--headers', dest='headers', help='comma separated names of CVS headers with (optional) types, if headers are omitted, first row of the CSV file is assumed to contain the headers and all types are set to string. Available types are "string", "float", "integer" and "date"; Example of valid headers: name:string,age:integer,city:string. If type is omitted type is string by default.')

	args = parser.parse_args()
	
	import_csv(args.dbname, args.collection, args.headers, args.csv_file)