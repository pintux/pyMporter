## pyMporter, a python CSV to MongoDB importer

This minimalist tool allows to import a CSV (comma separated) file to a MongoDB database with headers and simple types specification. Types are reflected on specified database collection.
The mongoimport tool distributed with MongoDB (vers. <= 2.4.6) doesn't allow to specify data values types.


### Prerequisites
In order to launch the tool the following python modules are needed:

- pymongo
- python-dateutil


### Usage

python pyMporter.py [-h] [--dbname DBNAME] [--collection COLLECTION]
                    [--headers HEADERS]
                    csv_file



positional arguments:
  csv_file

optional arguments:
  -h, --help            show this help message and exit

  --dbname DBNAME       MongoDB database name to use, default is NewDB;

  --collection COLLECTION
                        MongoDB collection name to import data to;

  --headers HEADERS     comma separated names of CVS headers with (optional)
                        types in the form of <header_name:type>, if headers are omitted, first row of the CSV
                        file is assumed to contain the headers and all types
                        are set to string. 
                        Available types are "string",
                        "float", "integer" and "date";

                        Example of valid headers: 

                        name:string,age:integer,city:string

                        id:integer,descr:string,date:date

                        If type is omitted type is string by default.


###Notes and limitations (v.1.0)
- it connects only to local MongoDB databases, at default port;
- compared to mongoimport tool, distributed with MongoDB, it's quite slow, but mongoimport doesn't support values type specification;
- the number of headers must match the number of comma-separated values in the CSV file;



###Examples

####1
With types specification:
python pyMporter.py --dbname MyDB --collection people --headers id:string,firstname:string,secondname:string,music:string,age:integer,date:date people.csv 


####2
Only headers without types specification, all values are set to "string":
python pyMporter.py --dbname MyDB --collection people --headers id,firstname,secondname,music,age,date people.csv



