#!/usr/bin/env python
# -*- coding: utf-8 -*-

# users.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This script lets us explore the data a little bit more
We will see out how many unique 'v' values each 'k' key contains
We will also generate the complete lists of unique elements that will help us understanding the kind of information we have
The function process_map will return a dictionary of sets of unique values found
'''

import xml.etree.cElementTree as ET
import pprint
import re
import os
from collections import OrderedDict
from collections import defaultdict

DATAFILE = 'Data/milan_italy_big.osm'

def get_user(element):
	return element.get('uid')

def process_map(filename):
    users = set()
    results = defaultdict(set)
    for _, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way':
            if 'uid' in element.attrib:
                users.add(get_user(element))
            for child in element:
                if child.tag == 'tag':
                    for attrib in child.attrib:
                        if attrib == 'k':
                            results[child.get(attrib)].add(child.attrib.get('v'))
    return results,users

if __name__ == '__main__':
    results,users = process_map(DATAFILE)
    if not os.path.isdir('Output'):
        os.mkdir('Output')
    with open('Output/osm_unique_tags.json', 'w') as outfile:
        pprint.pprint (dict(OrderedDict(sorted(results.items()))),outfile)

    print "Unique 'k' values: " + str(len(results)) # Number of unique tag 'k' in 'node' and 'way' nodes
    print 
    print 'Unique users: ' + str(len(users))
    print 'Unique buildings: ' + str(len(results['building']))
    print 'Unique addr:city: ' + str(len(results['addr:city']))
    print 'Unique addr:street: ' + str(len(results['addr:street']))
    print 'Unique addr:postcode: ' + str(len(results['addr:postcode']))
    print 'Unique amenities: ' + str(len(results['amenity']))