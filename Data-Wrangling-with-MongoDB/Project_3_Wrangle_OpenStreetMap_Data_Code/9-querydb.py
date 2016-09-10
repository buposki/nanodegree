#!/usr/bin/env python
# -*- coding: utf-8 -*-

# querydb.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This code will execute the queries used in project summary using PyMongo
Before running the script, we first need to create and import the datafile with:
mongoimport --db udacity --collection milan --drop --file milan_italy_big.osm.json
'''

from pymongo import MongoClient

if __name__ == '__main__':	
	client = MongoClient('mongodb://localhost:27017')
	db = client.udacity
	print 'Number of contributors: ', len(db.milan.distinct('created.user')); print
	print 'Top 5 contributors'
	cursor = db.milan.aggregate([
		{'$group':{'_id':'$created.user','count':{'$sum':1}}},
		{'$sort':{'count':-1}},
		{'$limit':5}
		])
	for document in cursor:
		print(document)
	print
	count = 0
	cursor = db.milan.aggregate([{'$group':{'_id':'$created.user','count':{'$sum':1}}}, {'$sort':{'count':-1}}, {'$match':{'count':{'$eq':1}}}])
	for document in cursor:
		count += 1
	print 'Number of users with only 1 contribution: ' + str(count)
	print
	print 'Number of amenities: ' + str(len(db.milan.distinct('amenity')))
	print 'Top 10 amenities'
	cursor = db.milan.aggregate([
		{'$match': {'amenity':{'$exists':'True'}}},
		{'$group':{'_id':'$amenity','count':{'$sum':1}}},
		{'$sort':{'count':-1}},
		{'$limit':10}
		])
	for document in cursor:
		print(document)
	print
	print 'Number of buildings: ' + str(len(db.milan.distinct('building')))
	print
	print 'Top 10 buildings'
	cursor = db.milan.aggregate([
		{'$match': {'building':{'$exists':'True'}}},
		{'$group':{'_id':'$building','count':{'$sum':1}}},
		{'$sort':{'count':-1}},
		{'$limit':10}
		])
	for document in cursor:
		print(document)
	print
	print 'Number of shops: ' + str(len(db.milan.distinct('shop')))
	print
	print 'Top 10 shops'
	cursor = db.milan.aggregate([
		{'$match': {'shop':{'$exists':'True'}}},
		{'$group':{'_id':'$shop','count':{'$sum':1}}},
		{'$sort':{'count':-1}},
		{'$limit':10}
		])
	for document in cursor:
		print(document)
	print
	print 'Number of cuisines: ' + str(len(db.milan.distinct('cuisine')))
	print
	print 'Top 20 cuisines'
	cursor = db.milan.aggregate([
		{'$match':{'amenity':'restaurant'}},
		{'$match':{'cuisine':{'$exists':1}}},
		{'$group':{'_id':'$cuisine','count':{'$sum':1}}}, 
		{'$sort':{'count':-1}}, 
		{'$limit':20}
		])
	for document in cursor:
		print(document)
	print
	print 'Number of postcodes: ' + str(len(db.milan.distinct('address.postcode')))
	print
	print 'Top 10 postcode'
	cursor = db.milan.aggregate([
		{'$match': {'address.postcode':{'$exists':'True'}}},
		{'$group':{'_id':'$address.postcode','count':{'$sum':1}}},
		{'$sort':{'count':-1}},
		{'$limit':10}
		])
	for document in cursor:
		print(document)