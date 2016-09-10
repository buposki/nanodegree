#!/usr/bin/env python
# -*- coding: utf-8 -*-

# getdata.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This code will download - if needed - the OpenStreetMap XML files

We will download two different area:
 - a larger area (boundaries: 9.0603, 45.3808, 9.2728, 45.5256) representing the metropolitan area of Milan
 - a smaller area (boundaries: 9.1635, 45.4507, 9.2076, 45.4824) that due its small size will speed up coding and testing
'''

import requests
import os

def getfile(link,filename):
	response = requests.get(link,stream=True)
	# Check if URL exists and give a ok status
	if response.status_code == 200:
		print 'Downloading %s' % link
		with open(filename, 'wb') as f:
			f.write(response.content)
			print 'Download complete. File size: %d' % os.path.getsize(filename)
	else:
		print 'Error while retrieving datafile %s' %link

if __name__ == '__main__':
	if not os.path.isdir('Data'):
		os.mkdir('Data')
	if not os.path.isfile('Data/milan_italy_big.osm'):
		getfile('http://overpass-api.de/api/map?bbox=9.0603,45.3808,9.2728,45.5256','Data/milan_italy_big.osm')
	if not os.path.isfile('Data/milan_italy_small.osm'):
		getfile('http://overpass-api.de/api/map?bbox=9.1635,45.4507,9.2076,45.4824','Data/milan_italy_small.osm')