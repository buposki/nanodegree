#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
We use this script to wrangle the data, transform their shape and export to a JSON file
We address 17 requirement/changes to datafile with a single iteration loop
Resulting JSON will be written in Data/FILENAME.json
'''

import xml.etree.cElementTree as ET
import re
import codecs
import json
import os
from collections import defaultdict

DATAFILE = 'Data/milan_italy_big.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'(^([a-z]|_)*):(([a-z]|_)*$)')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ 'version', 'changeset', 'timestamp', 'user', 'uid']
TAGDROP = [ 'addr:floor', 'addr:full', 'addr:interpolation', 'addr:state', 'addr:unit']
STREETMAPPING = { 'VIa': 'Via',
            'via': 'Via',
            'VIale': 'Viale',
            'Largo Volontari del sangue': 'Largo Volontari del Sangue',
            'Corso Lordi': 'Corso Lodi',
            'Leonardo Da Vinci': 'Leonardo da Vinci',
            'Piazza otto novembre': 'Piazza 8 Novembre',
            'Via Don G. Casaleggi': 'Via Don Giacomo Casaleggi',
            'Via Edmondo de Amicis': 'Via Edmondo De Amicis', # Use to check
            u'Via Enrico No\xeb': u'Via Enrico N\xf6e',
            "Via Fra' Riccardo Pampuri": 'Via Fra Riccardo Pampuri',
            'Via Leone Tolstoj': 'Via Leone Tolstoi',
            'Via Luigi Luzzati': 'Via Luigi Luzzatti',
            'Via Varesina 214': 'Via Varesina'
            }

def shape_element(element):
    node = {}
    # [Req.1] We will process only 2 types of top level tags: 'node' and 'way'
    if element.tag == 'node' or element.tag == 'way' :        
        # [Req.2] Set 'type' with value = node type ('node' or 'way')
        node['type']=element.tag
        # For each attrib in node
        for attrib in element.attrib:
            # [Req.3] Attributes for latitude ('lat') and longitude ('lon') should be added to a 'pos' array as float
            if attrib == 'lat':
                if 'pos' not in node:
                    node['pos'] = [None,None]
                node['pos'][0] = float (element.attrib['lat'])
            elif attrib == 'lon':
                if 'pos' not in node:
                    node['pos'] = [None,None]
                node['pos'][1] = float (element.attrib['lon'])
            # [Req.4] Attributes in the CREATED array should be grouped under a key 'created'
            elif attrib in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][attrib]=element.attrib[attrib]
            # [Req.5] All other attributes of 'node' and 'way' should be turned into regular key/value pairs
            else:
                node[attrib]=element.attrib[attrib]
        # We need to look in 'k' for each 'tag' nodes to find the addr:xxx tags we have to group
        for tag in element.iter('tag'):
            if 'k' in tag.attrib:
              # [Req.6] If 'k' in 'tag' node contain problematic char, it will be dropped
              if problemchars.match(tag.attrib['k']):
                  continue
              # [Req.7] If 'k' in 'tag' node in TAGDROP it will be dropped
              elif tag.attrib['k'] in TAGDROP:
                  continue
              else:
                 # If there are no problematic char and tag has not to be dropped
                 # [Req.8] If k attributes is in the form addr:x it will converted in an array 'address'
                 re = lower_colon.match(tag.attrib['k'])
                 # If it is in form xxx:xxx - we use group() to extract the part before the colon and the part after the colon
                 if re:
                     # Process all tags starting with addr:
                     first_key=re.group(1)
                     second_key=re.group(3)
                     # if there is a second ':' that separates the type/direction of a street, the tag should be ignored
                     if lower_colon.match(second_key):
                        continue
                     elif first_key == 'addr':
                         if not 'address' in node.keys():
                             node['address'] = {}
                         # [Req.17] Fix addr.street using STREETMAPPING
                         if second_key == 'street':
                            if tag.attrib['v'] in STREETMAPPING:
                                node['address']['street'] = STREETMAPPING[tag.attrib['v']]
                            else: 
                                node['address']['street'] = tag.attrib['v']
                         # [Req.13] Fix postcodes 20100
                         if second_key == 'postcode' and tag.attrib['v'] == '20100':
                             continue
                         # [Req.13] Fix postcodes 2090
                         elif second_key == 'postcode' and tag.attrib['v'] == '2090':
                             node['address'][second_key] = '20090'
                         # [Req.14] Fix addr:city
                         elif second_key == 'city' and tag.attrib['v'] == 'milano':
                             node['address'][second_key] = 'Milano'
                         # [Req.15] Fix addr:province
                         elif second_key == 'city' and tag.attrib['v'] == 'MI':
                             node['address'][second_key] = 'Milano'
                         else:
                             node['address'][second_key] = tag.attrib['v']
                     # there is a lower_colon.match for something different from 'addr'
                     else:
                         # replace ':'' with '__'
                         node[first_key + '__' + second_key] = tag.attrib['v']
                 else:
                    # other k values (except type that we import renamed in k_type)
                    # [Req.9] If k attributes is named 'type', rename it with 'k_type'
                    if tag.attrib['k'] == 'type':
                      node['k_type'] = tag.attrib['v']
                    # [Req.10] If k attribute is named 'comment.it:2', rename it with 'comment:it:2'
                    elif tag.attrib['k'] == 'comment.it:2':
                      node['comment:it:2'] = tag.attrib['v']
                    # [Req.11] If k attribute is named 'step.condition', rename it with 'step_condition'
                    elif tag.attrib['k'] == 'step.condition':
                      node['step_condition'] = tag.attrib['v']
                    else:
                      node[tag.attrib['k']] = tag.attrib['v']
        # [Req.12] If node contains nd tag, there will be transformed into an array
        for tag in element.iter('nd'):
            if not 'node_refs' in node.keys():
                node['node_refs'] = []
            if 'ref' in tag.attrib:
             node['node_refs'].append(tag.attrib['ref'])
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # Define the file for output writing
    file_out = '{0}.json'.format(file_in)
    # Initialize data array
    data = []
    # Open file for writing        
    with codecs.open(file_out, 'w') as fo:
            # For each element in OSM file (process at end event)
            for event, element in ET.iterparse(file_in):
                el = shape_element(element)
                if el:
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+'\n')
                    else:
                        fo.write(json.dumps(el) + '\n')
                # Clear memory if we end processing an element
                if event=='end' and (element.tag == 'way' or element.tag == 'node'):
                  element.clear()                
    return data

if __name__ == '__main__':
    data = process_map(DATAFILE, False)
    print 'File exported.'
