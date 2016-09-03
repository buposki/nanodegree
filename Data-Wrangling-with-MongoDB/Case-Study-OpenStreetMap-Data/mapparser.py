#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mapparser.py
# Data Wrangling with MongoDB (Udacity.com)
# Project 3: OpenStreetMap Data Case Study
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.
Note that your code will be tested with a different data file than the 'example.osm'
"""

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

def count_tags(filename):
    # We use defaultdict so that we don't need to check if an element with same tag already exists
    tag_count = defaultdict(int)
    # Iter along elements and increment tag count
    for _, element in ET.iterparse(filename):
        # Increment tag count by 1 - As we initialize tag_count with defaultdict, tag doesn't need to be already in dictionary
        tag_count[element.tag] += 1
        # Clear element from memory. It (really) speeds up execution and avoid computer locking due low memory
        element.clear()
    return dict(tag_count)

def test():
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

if __name__ == "__main__":
    test()
