#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tags.py
# Data Wrangling with MongoDB (Udacity.com)
# Project 3: OpenStreetMap Data Case Study
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

import xml.etree.cElementTree as ET
import pprint
import re

"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""

# We define three RegExp to match strings: 
# lower, will match strings composed only by [a-z] and _
# lower_colon, will match stings in the form string:string accepting strings composed only by [a-z] and _ on both sides of colon
# problemchars, will match strings containing one of a problematic char
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]') # match strings containing problematic chars

def key_type(element, keys):
    # We check for 'k' attribute in element "tag" to check for any problematic char
    if element.tag == "tag":
        key = element.attrib['k']
        if lower.match(key):
            keys["lower"] = keys["lower"] + 1
        elif lower_colon.match(key):
            keys["lower_colon"] = keys["lower_colon"] + 1
        elif problemchars.match(key):
            keys["problemchars"] = keys["problemchars"] + 1
        else:
            keys["other"] = keys["other"] + 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        element.clear()
    return keys

def test():
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}

if __name__ == "__main__":
    test()