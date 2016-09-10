#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkdata.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This code will execute queries to check the import
Before running the script, we first need to create and import the datafile with:
mongoimport --db udacity --collection milan --drop --file milan_italy_big.osm.json
'''

from pymongo import MongoClient

if __name__ == '__main__':
	client = MongoClient('mongodb://localhost:27017')
	db = client.udacity
	
	# Set to verify import - It should return same information of scripts (except for addr:city and addr:postcode where we expect a different number due the cleaning)
	print "Nodes in db (with type 'node'): ",db.milan.find({'type':'node'}).count() # It should match node [752505]
	print "Nodes in db (with type 'way'): ",db.milan.find({'type':'way'}).count() # It should match way [133735]
	print 'Total nodes in db: ', db.milan.find().count() # It should match 2016-09-09T09:21:05.329+0200    imported 886240 documents
	print 'Unique users: ', len(db.milan.distinct('created.user')) # It should match Unique users: 1086
	print 'Unique buildings: ', len(db.milan.distinct('building')) # It should match Unique buildings: 66
	print 'Unique addr:city ', len(db.milan.distinct('address.city')) # It should match Unique addr:city: 21 - 1 (the 'milano' transformed in 'Milano')
	print 'Unique addr:street ', len(db.milan.distinct('address.street')) # It should match Unique addr:street: 2103
	print 'Unique postcode', len(db.milan.distinct('address.postcode')) # It should match Unique addr:postcode 54-2 (One deleted, one renamed to already existing postcode)
	print 'Unique amenity', len(db.milan.distinct('amenity')) # It should match Unique amenities: 107