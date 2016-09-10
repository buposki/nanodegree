#!/usr/bin/env python
# -*- coding: utf-8 -*-

# audit.py
# Data Wrangling with MongoDB (Udacity.com)
# Project 3: OpenStreetMap Data Case Study
#
# Amodiovalerio Verde
# amodiovalerio.verde@gmail.com

'''
To audit our data, we will print the addr:tags count and
use mapping to check how many street names will be renamed
'''
import xml.etree.cElementTree as ET
import re
import os
import pprint
import json
from collections import defaultdict
from collections import OrderedDict

OSMFILE = "Data/milan_italy_big.osm"
# Changed Regexp to match italian street denomination
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)
mapping_count=0
expected_count=0

# We will expect these words as first part of street names
expected = ["Corso", "Via", "Largo", "Piazza", "Galleria", "Viale", "Vicolo", "Piazzale", "Piazzetta", 
            "Alzaia", "Bastioni", "Cortile", "Foro", "Ripa", "Passaggio", "Strada", "Residenza"]

mapping = { "VIa": "Via",
            "via": "Via",
            "VIale": "Viale",
            "Largo Volontari del sangue": "Largo Volontari del Sangue",
            "Corso Lordi": "Corso Lodi",
            "Leonardo Da Vinci": "Leonardo da Vinci",
            "Piazza otto novembre": "Piazza 8 Novembre",
            "Via Don G. Casaleggi": "Via Don Giacomo Casaleggi",
            "Via Edmondo de Amicis": "Via Edmondo De Amicis",
            u"Via Enrico No\xeb": u"Via Enrico N\xf6e",
            "Via Fra' Riccardo Pampuri": "Via Fra Riccardo Pampuri",
            "Via Leone Tolstoj": "Via Leone Tolstoi",
            "Via Luigi Luzzati": "Via Luigi Luzzatti",
            "Via Varesina 214": "Via Varesina"
            }

# Fill street_type dict with address not matching prefix (in expected)
# and address in mapping
def audit_street_type(street_types, street_name):
    global mapping_count
    global expected_count
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_name in mapping:
            street_types[street_type].add(street_name)
            mapping_count += 1
        if street_type not in expected:
            street_types[street_type].add(street_name)
            expected_count +=1

# Returns true if elem is an 'addr:' element
def is_addr_elem(elem):
    return (re.compile(r"addr:(.*)").match(elem))

# If name is in mapping, return the corrected value
def update_name(name, mapping):
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for abbrv in sorted_keys:
        if(abbrv in name):
            return name.replace(abbrv, mapping[abbrv])
    return name

def audit(osmfile):
    osm_file = open(osmfile, "r")
    addr_count = defaultdict(lambda: defaultdict(int))
    for _, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                a = is_addr_elem(tag.attrib['k'])
                if a:
                    if a.group(1) in addr_count:
                        addr_count[a.group(1)][tag.attrib['v']] += 1
                    else:
                        addr_count[a.group(1)][tag.attrib['v']] = 1
        elem.clear()
    return addr_count

def audit_addrkey(osmfile):
    osm_file = open(osmfile, "r")
    addr_count = defaultdict(set)
    for _, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way" or elem.tag == "relation":
            for tag in elem.iter("tag"):
                a = is_addr_elem(tag.attrib['k'])
                if a:
                    if a.group(1) in addr_count:
                        addr_count[a.group(1)] += 1
                    else:
                        addr_count[a.group(1)] = 1
        elem.clear()
    return addr_count

#  For each element of type 'node' or 'way', it looks for a 'addr:street value'
#  When found it audit street type, passing the dictionary and the value
def audit_streetnames():
    if not os.path.isdir("Output"):
        os.mkdir("Output")    
    # audit street names and put results in st_types
    # st_types contains a dictionary with all matches that will be changed
    
    osm_file = open(OSMFILE, "r")
    st_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # This will audit all addr:street tag
                if tag.attrib['k'] == "addr:street":
                    audit_street_type(st_types, tag.attrib['v'])
        elem.clear()
    
    #st_types = auditstreet(OSMFILE)
    with open('Output/osm_audit_streetnames.txt', 'w') as outfile:
        for st_type, ways in st_types.iteritems():
            for name in ways:
                better_name = update_name(name, mapping)
                string = name + " => " + better_name
                outfile.write(string.encode('utf8'))
                outfile.write("\n")

if __name__ == '__main__':
    # Calculate the number of street names that will be renamed
    audit_streetnames()
    print 'Renamed due mapping (Renamed streets): ' + str(mapping_count)
    print 'Renamed due expected (Renamed street prefixes): ' + str(expected_count)
    
    # Print and save the count of different addr:part elements
    addr_types = audit_addrkey(OSMFILE)
    data_as_dict = json.loads(json.dumps(addr_types))
    with open('Output/osm_addr_tags_count.json', 'w') as outfile:
        pprint.pprint (data_as_dict,outfile)
    print
    print "Count of addr:tags"
    pprint.pprint(data_as_dict)

    # Print and save the count and unique values for all addr:part elements
    addr_types = audit(OSMFILE)
    data_as_dict = json.loads(json.dumps(addr_types))
    with open('Output/osm_addr_tags_values_count.json', 'w') as outfile:
        pprint.pprint (data_as_dict,outfile)
    print
    print "Count of addr:tags values"
    pprint.pprint(data_as_dict)
