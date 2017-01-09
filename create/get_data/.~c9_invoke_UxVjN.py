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
    CKAN metadata laid out in columns
    CKAN [metadata] formatted for creation
Create Metadata
    CREATE call to CKAN
    reports of success, failure for each CREATE call
"""

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

knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    knack_api_key= os.environ['KNACK_API_KEY']



# candidate for library...
# function to create multiple values in case relation of object to 
# dataset is 'many'.   Each value will be separated with pipe character.
def list_values(list):
    count = len(list)
    value_list = []
    
    if count:
        if count > 1:
            for obj in list:
                value_list.append(str(obj['identifier']))
        else:
            value_list.append(str(list[0]['identifier']))
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
    
    # both id and key are needed.  Id is for the specific application.
    # the key is to gain 'read' and 'write' permissions
    knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    knack_api_key= os.environ['KNACK_API_KEY']
    
    
    # data_string = urllib.quote(json.dumps(payload))
    
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
    
    knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    knack_api_key= os.environ['KNACK_API_KEY']
    
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
    knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    knack_api_key= os.environ['KNACK_API_KEY']
    
    
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
    

# with open('titles.txt', 'w') as titles:
#     with open('descriptions.txt', 'w') as descriptions:
#         for record in records:
#             titles.write('%s\n' % record['field_5'].strip())
#             descriptions.write('%s\n%s\n\n' % (record['field_5'].strip(), record['field_6'].strip()))
        
with open('knack_metadata.txt', 'w') as knack:
    knack.write('title\ttype\tdesc\tprovider\tsource\tpublisher\tclassification'
    '\topen\tupdate freq\tfrom\tto\tcoverage notes\ttopic\tgeo coverage\tcontact point'
    '\tcontact email\tcontact phone\n')
    for record in records:
        title = record['field_5_raw'].strip()
        btype = list_values(record['field_152_raw'])
        
        # Instead include object reference.  Together with field (field_6), can easily query
        # interrupt formatting for report
        # desc =  record['field_6_raw'].strip()
        # Description to large in most cases to include in file.
        # Instead include object reference.  Together with field (field_6), can easily query
        # for description to create notes parameter.
        desc = record['id']
        provider = list_values(record['field_186_raw'])
        source = list_values(record['field_164_raw'])
        publisher = list_values(record['field_205_raw'])
        classification = list_values(record['field_155_raw'])
        open_value = record['field_308_raw']
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
        topics = list_values(record['field_146_raw'])
        location = list_values(record['field_136_raw'])
        
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
                print(contact_name)
                try:
                    contact_info_list = get_contact_info(record['field_147_raw'])
                    
                except:
                    e = sys.exc_info()[0]
                    contact_info_list = ['none', 'none']
                    print(e)
            else:
                print(record['field_5']+' has no contact')
                contact_name = 'none'
                contact_info_list = ['none', 'none']
        else:
            print(record['field_5'] + 'has no contact field key')
            contact_name = 'none'
            contact_info_list = ['none', 'none']
        
        knack.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}"
            "\t{14}\t{15}\t{16}\n".format(
            title, desc, btype, provider, source, publisher, classification, open_value,
            freq, temp_from, temp_to, temporal_notes, topics, location, contact_name, contact_info_list[0],
            contact_info_list[1]))



