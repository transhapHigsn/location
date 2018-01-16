# locatorApi

To load the .csv file run the following sql commands in postgres terminal
=========================================================================
 
*  CREATE TABLE location
*  ( key Text,
*    place_name text PRIMARY_KEY,
*    admin_name1 text UNIQUE NOT NULL,
*    latitude real UNIQUE NOT NULL,
*   longtitude real UNIQUE NOT NULL,
*    accuracy integer
* );
  
 
 *  COPY location
 *  FROM '/home/username/Documents/IN.csv' DELIMITER ',' CSV HEADER;


To start the server run command
================================

* export FLASK_APP=app.py
* export FLASK_DEBUG=True
* export flask run

Note: Currently, testing can only be done while server is running.



References taken from stackoverflow, official flask documentation, postgres documentation and few other blogs.
