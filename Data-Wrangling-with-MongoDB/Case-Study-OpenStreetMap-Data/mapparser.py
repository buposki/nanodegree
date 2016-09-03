#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mapparser.py
# Data Wrangling with MongoDB (Udacity.com)
# Project 3: OpenStreetMap Data Case Study
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

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

    return tag_count

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