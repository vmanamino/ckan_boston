"""
The aim is to create dataset metadata on the Boston Open Data Hub.
This script will use metadata already created on a Knack database.
To that end, I will use the Knack API to get that data.
Transformation is necessary to create the Boston Open Data Hub metadata.
Please see the mapping created for this task.

transformation requires the following steps:

Get Data
    Knack GET calls, and analysis of responses -- Done
Prepare Data
    Knack data laid out in columns -- Done
    Mapping to CKAN and necessary transformations -- Current
    CKAN metadata laid out in columns -- irrelevant
    CKAN [metadata] formatted for creation
Create Metadata
    CREATE call to CKAN
    reports of success, failure for each CREATE call
    
include prep_data.py script in this and write directly to CKAN
"""

import json, os
import pprint
from slugify import slugify
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

knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
knack_api_key= os.environ['KNACK_API_KEY']

# deal with empty values, currently understood as empty strings
# pass only the values in, not the key value pair
def value_none(val):
    value = ''
    if not val:
        value = 'none'
    else:
        value = val
    return value

# candidate for library...
# function to create multiple values in case relation of object to 
# dataset is 'many'.   Each value will be separated with pipe character.
def list_values(list_obj):
    count = len(list_obj)
    value_list = []
    
    # assumes that with first element empty, no values at all
    if count and list_obj[0]['identifier']:
        if count > 1:
            for obj in list_obj:
                value_list.append(str(obj['identifier']))
        else:
            value_list.append(str(list_obj[0]['identifier']))
        return_obj = value_list
    else:
        return_obj = "none"
    return return_obj

def date_formatted(time_obj):
    stamp = time_obj['unix_timestamp']
    temporal = time.strftime('%Y-%m-%d', time.gmtime(stamp/1000.))
    return temporal

def get_contact_info(obj):
    attributes = obj
    
    # contact is only one per dataset in our scheme, so can be confident in first place of all info
    contact_identifier = attributes[0]['id']
    
    # will have to prep request to add ID and KEY as headers
    url = 'https://api.knack.com/v1/objects/object_36/records/'+contact_identifier
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    response = json.loads(r.read())
    
    contact_info = get_gov_entity_info(response['field_216_raw'][0]['id'])
    
    # contact_info = json.loads(gov_entity_response.read())
    
    return contact_info
    
def get_gov_entity_info(identifier):
    url = 'https://api.knack.com/v1/objects/object_3/records/'+identifier
    
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    response = json.loads(r.read())
    
    info = []
    if response['field_12_raw']['email']:
        email = response['field_12_raw']['email']
        info.append(email)
    else:
        info.append('none')
    if response['field_13_raw']['formatted']:
        phone = response['field_13_raw']['formatted']
        info.append(phone)
    else:
        info.append('none')
        
    return info
    
def get_knack_data(page="1"):
    # both id and key are needed.  Id is for the specific application.
    # the key is to gain 'read' and 'write' permissions
    # knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    # knack_api_key= os.environ['KNACK_API_KEY']
    
    
    # data_string = urllib.quote(json.dumps(payload))
    
    # will have to prep request to add ID and KEY as headers
    url = 'https://api.knack.com/v1/objects/object_2/records?page='+page
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    return r    
    
"""
functions to assign fixed values to parameters, later to be used in
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

"""
CKAN parameters
"""
 # title_translated-en: "string" ; mandatory
title_translated = ""

# name: "slugged-title" ; required
name = ""

# btype: ["fixed values"]
btype = []

# notes_translated: {"en":"string"}
notes_translated = ""

# provider: "string" (fixed value) ; mandatory
provider = ""

# source: ["fixed values"]
source = []

# owner_org: "string" (fixed value); required 
owner_org = ""

# classification: "string" (fixed value)
classification = ""

# isopen: boolean true or false
isopen = False

# accrual_periodicity: "string" (fixed value)
freq = ""

 # temporal_from: "formatted date string"
temp_from = ""
        
# temporal_to: "formatted date string"
temp_to = ""
        
# temporal_notes: {"en": "string"}
temp_notes = ""
        
# theme: ["fixed values"]
topic = []
        
# location: ["fixed values"]
geo = []
        
# contact_point: "string" (fixed value)
contact = "" # raw: string mandatory as contact_point
        
# contact_point_email: "string" (email)
email = "" # raw: string (email) mandatory as contact_point_email
        
# contact_point_phone: "string" (phone number)
phone = "" # raw string (phone number)

# tags: ["string", "string"]
tags = []

"""
start the work of getting Knack data
"""
response = get_knack_data()
data = json.loads(response.read())
pages = data['total_pages']

if pages > 1:
    
    # first page of records
    records = data['records']
    range_end_boundary = pages + 1
    
    # start on second page always
    for i in range(2, range_end_boundary):
        response = get_knack_data(str(i))
        data = json.loads(response.read())
        records += data['records']
    
else:
    records = data['records']

"""
assign knack data to variables/values for ckan parameters
"""

with open('knack_metadata.txt', 'w') as knack:
    knack.write('title\ttype\tdesc\tprovider\tsource\tpublisher\tclassification'
    '\topen\tupdate freq\tfrom\tto\tcoverage notes\ttopic\tgeo coverage\tcontact point'
    '\tcontact email\tcontact phone\tkeywords\n')
    for record in records:
        title = record['field_5_raw'].strip()
        title_translated = title
        name = slugify(title)
        # print(name)
        dataset_types = list_values(record['field_152_raw'])
        # call the types function above
        
        # description assigned but not written because of hidden characters which 
        # interrupt formatting for report
        # desc =  record['field_6_raw'].strip()
        # Description to large in most cases to include in file.
        # Instead include object reference.  Together with field (field_6), can easily query
        # for description to create notes parameter.
        desc = record['id']
        provider = list_values(record['field_186_raw'])
        # print(provider)
        source = list_values(record['field_164_raw'])
        publisher = list_values(record['field_205_raw'])
        classification = list_values(record['field_155_raw'])
        open_value = record['field_308_raw']
        open_value =  value_none(open_value)
        freq = list_values(record['field_139_raw'])
        
        """
        dealing with date info
        """
        if record['field_121_raw']:
            temp_from = date_formatted(record['field_121_raw'])
        else:
            temp_from = 'none'
        if record['field_122_raw']:
            temp_to = date_formatted(record['field_122_raw'])
        else:
            temp_to = 'none'
        
        temporal_notes = record['field_159_raw'].strip()
        temporal_notes = value_none(temporal_notes)
        topics = list_values(record['field_146_raw'])
        location = list_values(record['field_136_raw'])
        keywords = list_values(record['field_321_raw'])
        
        """
        Get contact info.  Was not able to get Knack filter to work.
        Display name for Gov Entity (Object 3) which is the parent of Contact is
        the Title, which is appropriate for two reasons.  1: Labels can be many and for different
        purposes, the title is single and authoritative.  The value must be unique.
        2: Since Title is Display Name and unique, it can be queried on from the value supplied to Dataset (Object 2),
        and any changes to the Title will cascade to the Contact (Object 36), 
        and in turn to Dataset (Object 2)
        """
        # there is only one contact per dataset, so can be confident of first place in list
        
        contact_name = ''
        contact_info_list = []
        
        if record.has_key('field_147'):
            if (record['field_147']):
                contact_name = record['field_147_raw'][0]['identifier'].strip()
                # print(contact_name)
                try:
                    contact_info_list = get_contact_info(record['field_147_raw'])
                    
                except:
                    e = sys.exc_info()[0]
                    contact_info_list = ['none', 'none']
                    # print(e)
            else:
                # print(record['field_5']+' has no contact')
                contact_name = 'none'
                contact_info_list = ['none', 'none']
        else:
            # print(record['field_5'] + 'has no contact field key')
            contact_name = 'none'
            contact_info_list = ['none', 'none']
        
        knack.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}"
            "\t{14}\t{15}\t{16}\t{17}\n".format(
            title, btype, desc, provider, source, publisher, classification, open_value,
            freq, temp_from, temp_to, temporal_notes, topics, location, contact_name, contact_info_list[0],
            contact_info_list[1], keywords))



