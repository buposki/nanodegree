# tags.py
# Data Wrangling with MongoDB (Udacity.com)
# Project 3: OpenStreetMap Data Case Study
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

import xml.etree.cElementTree as ET
import pprint
import re

# We define three RegExp to match strings: 
lower = re.compile(r'^([a-z]|_)*$') # match strings composed only by [a-z] and _
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$') # match strings in the form string:string accepting only strings [a-z] and _ on both sides of colon
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
        pass
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