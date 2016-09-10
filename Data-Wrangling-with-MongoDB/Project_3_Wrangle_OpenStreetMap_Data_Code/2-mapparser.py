#!/usr/bin/env python
# -*- coding: utf-8 -*-

# mapparser.py
# Data Wrangling with MongoDB (Udacity.com)
# Final Project
#
# Amodiovalerio Verde (amodiovalerio.verde at gmail.com)

'''
This code will read the XML file for basic info on its structure

It will count nodes, structure and the attributes count for each node
'''

import os
import json
import xml.etree.cElementTree as ET
from collections import defaultdict
from xml.etree.ElementTree import iterparse

DATAFILE = 'Data/milan_italy_big.osm'

# The Nodes_Count function will create a dictionary of dictionaries describing the structure of the file
# Dictionary has key = depth and values = dictionaries. Last dictionary will contain the node names and count
# This will give us a first overview of the different levels nodes and number of nodes
# It will return the dictionary of dictionaries
def Nodes_Count(filename):
    if not os.path.isfile(filename):
        print 'File ' + filename + ' not found.'
        return None
    depth=0
    nodes=0
    nodes_dict = defaultdict(lambda: defaultdict(int))
    # We use start and end events to record the depth level we are in
    for (event, node) in iterparse(filename, ['start', 'end']):
        if event=='start': 
            nodes += 1
            nodes_dict[depth][node.tag] += 1
            depth += 1
        if event=='end':
            depth -= 1
            node.clear()
    return nodes_dict

# Pretty print nodes_dict
def Nodes_Count_Print(nodes_dict):
    if not nodes_dict:
        return
    nodes = 0
    print 'Number of levels: ' + str(len(nodes_dict))
    print
    for a in nodes_dict:
        print 'Level: ' + str(a)
        for b in nodes_dict[a]:
            print '   ' + str(b) + ' [' + str(nodes_dict[a][b]) + ']'
            nodes += nodes_dict[a][b]
        print
    print 'Total number of nodes: ' + str(nodes)

# This function will count the number of attributes belonging to each tag
# It will return the dictionary of dictionaries, where first key is node, 
# second key is attrib and value is number of attributes for that node
def Nodes_Attrib_Count(filename):
    if not os.path.isfile(filename):
        print 'File ' + filename + ' not found.'
        return None
    nodes=0;depth=0;
    nodes_attrib = defaultdict(lambda: defaultdict(int))
    # We use both event 'start' and 'end' to keep track of the depth
    for (event, node) in iterparse(filename, ['start', 'end']):
        if event=='start': 
            for a in dict(node.attrib):
                nodes_attrib[node.tag][a] += 1
            nodes += 1
            depth += 1
        if event=='end':
            depth -= 1
            node.clear()
    return nodes_attrib

# Pretty print nodes_attrib
def Nodes_Attrib_Count_Print(nodes_attrib,limit=10):
    for a in nodes_attrib:
        print
        print 'Node: ' + str(a)
        print dict(nodes_attrib[a])
        print
        Nodes_Sample(DATAFILE,str(a),limit)

# Prints the first 'limit' nodes for each node type
def Nodes_Sample(filename,nodetag='node',limit=10):
    if limit==0:
        return None
    count=0
    for (event, node) in iterparse(filename, ['start',]):
        if node.tag == nodetag:
            print node.tag, node.attrib
            count += 1
        if count == limit: break
        node.clear()
    return count
    
if __name__ == '__main__':
    # Count XML Nodes in datafile and fill nodes_dict with structure info and pretty print nodes_dict
    nodes_dict=Nodes_Count(DATAFILE)
    Nodes_Count_Print(nodes_dict)

    # Count attribs for each node & pretty print nodes_attr and (optionally) example nodes for each node type
    nodes_attr=Nodes_Attrib_Count(DATAFILE)
    Nodes_Attrib_Count_Print(nodes_attr,0)

    # Write the structure info and attrib info to file
    if not os.path.isdir('Output'):
        os.mkdir('Output')
    with open('Output/osm_node_structure.json', 'w') as outfile:
        json.dump(nodes_dict, outfile)
    with open('Output/osm_attrib_by_node.json', 'w') as outfile:
        json.dump(nodes_attr, outfile)