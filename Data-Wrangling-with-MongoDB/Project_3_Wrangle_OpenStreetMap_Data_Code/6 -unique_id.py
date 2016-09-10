#!/usr/bin/env python
# -*- coding: utf-8 -*-

# unique_id.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
# Function 'is_attrib_unique' will tell us if the attrib has unique values
# It will print the number of unique and duplicate occurencies and
# returns False if not unique and True if unique
'''

from collections import defaultdict
from xml.etree.ElementTree import iterparse

DATAFILE='Data/milan_italy_big.osm'

def is_attrib_unique(filename,attrib):
    id_count=0
    unique_id=0
    dupe_id=0
    ids = defaultdict(int)
    # First fill a dictionary with count for unique id
    for (_, node) in iterparse(filename, ['start',]):
        if node.tag == 'way' or node.tag == 'node':
            for attr in dict(node.attrib):
                if attr == attrib:
                    id_count += 1
                    ids[node.attrib[attrib]] += 1
        node.clear()
    # Then, if count > 1 then there is a duplicate
    for k,v in ids.items():
        if v>1:
            dupe_id += 1
        else:
            unique_id += 1
    print 'Uid found: ' + str(id_count)
    print 'Unique uids: ' + str(unique_id)
    print 'Duplicate uids: ' + str(dupe_id)
    if dupe_id == 0:
        return True
    else:
        return False

# To verify if we can use 'id' as MongoDB unique id, we will check if it is unique
if __name__ == '__main__':
    print is_attrib_unique(DATAFILE,'id')