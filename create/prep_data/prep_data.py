"""
Need to create large payloads using Knack metadata, see /create/get_data/knack_metadata.txt
test with limited number of datasets, create test file /create/get_data/knack_metadata_test.txt
"""

"""
see curl.txt for curl request
"""
import csv
import json, os
import pprint
import sys
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

def list_metadata(field):
    
    return

with open('/home/ubuntu/workspace/code/ckan_boston/create/get_data/knack_metadata_test.txt') as knack_records:
    
    # 17 columns, each corresponding to ckan metadata
    data_in = knack_records.read().splitlines()
    # knack_records = csv.reader(knack_records, delimiter='\t')
    count = 0
    
    for line in data_in:
        if count:
            row = line.split('\t')
            title = row[0]
            dataset_type = row[1]
            obj_desc = row[2]
            print(obj_desc)
        
        count += 1