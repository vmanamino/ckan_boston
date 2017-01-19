"""
See patch_data_contact.py file for testing of this modules
"""

import json, os
import sys
import urllib2
import urllib
# this is where my keys are kept hidden from Github and this where my current modules are
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
reload(sys)
import keys

# Knack response header:
# Content-Type application/json; charset=utf-8
# I guess from this that character encoding is UTF-8
sys.setdefaultencoding('utf-8')

# CKAN API key
key = os.environ['CKAN_API_KEY'];

# Knack application id and API key
knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
knack_api_key= os.environ['KNACK_API_KEY']



def get_knack_dataset(ident):
   
    # will have to prep request to add ID and KEY as headers
    # had problems adding id as payload, should be tacked on at end
    url = 'https://api.knack.com/v1/objects/object_2/records/'+ident
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    return r    

# provide contact object 'field_147_raw' from Knack object_2 record, see get_knack_dataset
def get_contact_object(obj):
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
    
    # currently method call returns email and phone, in that order
    contact_info = get_gov_entity_info(response['field_216_raw'][0]['id'])
    
    contact_info.insert(0, attributes[0]['identifier'])
    
    contact_obj = Contact(contact_info[0], contact_info[1], contact_info[2])
    
    # contact_info = json.loads(gov_entity_response.read())
    
    return contact_obj
    
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
    
class Contact:
    def __init__(self, fn, email, phone):
        self.fn = fn
        self.email = email
        self.phone = phone