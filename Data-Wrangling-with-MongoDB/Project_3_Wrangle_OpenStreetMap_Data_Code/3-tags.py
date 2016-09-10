#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tags.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This code will read the XML file and gather information on nodes 'tag' and
more specifically, of their key/value values

We will count, print and export the list of all key values used by type
'''

import xml.etree.ElementTree as ET
import pprint
import re
import os
from collections import defaultdict
from collections import OrderedDict
import json

DATAFILE = 'Data/milan_italy_big.osm'

# RegExp to match keys:
# - composed by all lowercase and digits
# - that are in the form key:subkey where key and subkey are composed by all lowercase and digits
# - that contain characters that can lead to problems
lower = re.compile(r'^([a-z0-9]|_)*$')
lower_colon = re.compile(r'^([a-z0-9]|_)*:([a-z0-9]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

lower_dict = defaultdict(int)
lower_colon_dict = defaultdict(int)
problemchars_dict = defaultdict(int)
other_dict = defaultdict(int)

def key_type(element, keys):
    if element.tag == "tag":
        if re.search(problemchars, element.attrib['k']):
            keys['problemchars'] += 1
            problemchars_dict[element.attrib['k']] += 1
        elif re.search(lower, element.attrib['k']):        
            keys['lower'] += 1
            lower_dict[element.attrib['k']] += 1
        elif re.search(lower_colon, element.attrib['k']):
            m = re.search(lower_colon, element.attrib['k'])
            keys['lower_colon'] += 1
            lower_colon_dict[element.attrib['k']] += 1
        else:
            keys['other'] += 1                 
            other_dict[element.attrib['k']] += 1
    return keys

def process_map(filename):
    #initialize dictionary
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        # Process each node and pass the updated count of keys
        keys = key_type(element, keys)
        # Discard the element to clear memory and speed up processing
        element.clear()
    return keys

# Process file
if __name__ == '__main__':
    keys = process_map(DATAFILE)

    if not os.path.isdir("Output"):
        os.mkdir("Output")

    print "Keys by type"
    pprint.pprint(dict(keys))
    with open('Output/osm_k_tags_count_by_type.json', 'w') as outfile:
        pprint.pprint (dict(keys),outfile)
    print
    print "Lower Keys"
    pprint.pprint (dict(OrderedDict(sorted(lower_dict.items()))))
    with open('Output/osm_k_tags_lower.json', 'w') as outfile:
        pprint.pprint (dict(OrderedDict(sorted(lower_dict.items()))),outfile)
    print
    print "Lower Colon Keys"
    pprint.pprint (dict(OrderedDict(sorted(lower_colon_dict.items()))))
    with open('Output/osm_k_tags_lower_colon.json', 'w') as outfile:
        pprint.pprint (dict(OrderedDict(sorted(lower_colon_dict.items()))),outfile)
    print
    print "Problem Chars Keys"
    pprint.pprint (dict(OrderedDict(sorted(problemchars_dict.items()))))
    with open('Output/osm_k_tags_problemchars.json', 'w') as outfile:
        pprint.pprint (dict(OrderedDict(sorted(problemchars_dict.items()))),outfile)
    print
    print "Other Keys"
    pprint.pprint (dict(OrderedDict(sorted(other_dict.items()))))
    with open('Output/osm_k_tags_other.json', 'w') as outfile:
        pprint.pprint (dict(OrderedDict(sorted(other_dict.items()))),outfile)