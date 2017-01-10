"""
Need to create large payloads using Knack metadata, see /create/get_data/knack_metadata.txt
test with limited number of datasets, create test file /create/get_data/knack_metadata_test.txt

Move all this to get_data.py and create parameters on the fly sending the calls for each new dataset
one at a time, each row will be replaced by the Knack field
"""

"""
see curl.txt for curl request
"""

import ast
# import csv
import json, os
import pprint
import sys
from slugify import slugify
import time
import urllib2
import urllib
# this is where my keys are kept hidden from Github
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
import keys
reload(sys)

# Knack response header:
# Content-Type application/json; charset=utf-8
# I guess from this that character encoding is UTF-8
sys.setdefaultencoding('utf-8')

"""
important functions, perhaps later to be used in
building a library/module
"""

def classifications(entity):
    
    return

def frequencies(entity):
    
    return

# aka owner_org
def gov_entities(entity):
    
    
    return

def open_values(value):
    
    return

def providers(entity):
    
    return

def sources(entity):
    
    return

def themes(entity):
    
    return

# aka spatial

def locations(entity):
    
    return

def types(entity):
    
    return

knack_records = open('/home/ubuntu/workspace/code/ckan_boston/create/get_data/knack_metadata_test.txt')
slugs = open('slugs.txt', 'w')
    
    
    # 17 columns, each corresponding to ckan metadata
data_in = knack_records.read().splitlines()
    # knack_records = csv.reader(knack_records, delimiter='\t')
header = 0
    
for line in data_in:
    if header:
        row = line.split('\t')
        
        # title_translated-en: "string" ; mandatory
        title = row[0]
        
        # name: "slugged-title" ; required
        slugged = slugify(title)
        
        # btype: ["fixed values"]
        dataset_type = row[1] # list
        
        # notes_translated: {"en":"string"}
        obj_desc = row[2] # object id to retrieve actual description via Knack API
        
        # provider: "string" (fixed value) ; mandatory
        provider = row[3] # list mandatory
        # provider = ast.literal_eval(provider)
            
        # source: ["fixed values"]
        source = row[4] # list
        
        # owner_org: "string" (fixed value); required 
        publisher = row[5] # list
        
        # classification: "string" (fixed value)
        classification = row[6] # list
        
        # isopen: boolean true or false
        open_value = row[7] # raw value: string
        
        # accrual_periodicity: "string" (fixed value)
        freq = row[8] # list
        
        # temporal_from: "formatted date string"
        temp_from = row[9] # formatted date string
        
        # temporal_to: "formatted date string"
        temp_to = row[10] # foratted date string
        
        # temporal_notes: {"en": "string"}
        temp_notes = row[11] # raw: string
        
        # theme: ["fixed values"]
        topic = row[12] # list
        
        # location: ["fixed values"]
        geo = row[13] # list
        
        # contact_point: "string" (fixed value)
        contact = row[14] # raw: string mandatory as contact_point
        
        # contact_point_email: "string" (email)
        email = row[15] # raw: string (email) mandatory as contact_point_email
        
        # contact_point_phone: "string" (phone number)
        phone = row[16] # raw string (phone number)
        
        
    header += 1