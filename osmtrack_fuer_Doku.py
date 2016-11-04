#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 2016
Last Edit on Fri Oct 6 2016

@author: bjoern
"""

import paho.mqtt.publish as mqtt
import os, json, cgi, cgitb
import datetime
from  wsgiref.simple_server import make_server

# osmupload ist der Handler der bei eingehenden Calls auf Port 8001 aufegrufen wird
def osmupload(env, start_response):
	userid ={'username':"angeben",'password':"angeben"}
	topic="owntracks/bjoern/osmand"
	hostname="localhost"
	port=8883
	data={
    	"_type" : "location",
    	"alt"   : 0,
    	"lat"   : 34.533333,
    	"lon"   : 69.166666,
    	"tid"   : "bp",
		"tst"   : 0
	}
	#Zuweisung der aktuellen Daten
   htmldata = cgi.FieldStorage(environ=env)
	data['lat']=htmldata.getvalue('lat')
	data['lon']=htmldata.getvalue('lon')
	data['alt']=htmldata.getvalue('alt')
	data['tst']=int(long((htmldata.getvalue('tst')))/1000)-int(datetime.datetime.utcfromtimestamp(0).strftime('%s'))
	if (data['lat']!=None) and (data['lon']!=None):
    		#Json als String formatieren
    		datastr=json.dumps(data)
    		print datastr
    		mqtt.single(topic,payload=datastr,auth=userid,port=port,hostname=hostname)
    		status = '200 OK'  # HTTP Status
    		headers = [('Content-type', 'text/plain; charset=utf-8')]  # HTTP Headers
    		start_response(status, headers)
		return []
	else:
    		status = '500'  # HTTP Status
    		headers = [('Content-type', 'text/plain; charset=utf-8')]  # HTTP Headers
    		start_response(status, headers)
		return []


#hier wird der Server erzeugt und der Handler angegeben
httpd=make_server('',8001,osmupload)
print("Serving on port 8001...")
#enbles CGI Debugging
cgitb.enable()
# Serve until process is killed
httpd.serve_forever()
