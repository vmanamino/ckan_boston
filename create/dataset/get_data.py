"""
The aim is to create dataset metadata on the Boston Open Data Hub.
This script will use metadata already created on a Knack database.
To that end, I will use the Knack API to get that data.
Transformation is necessary to create the Boston Open Data Hub metadata.
Please see the mapping created for this task.
"""

import json, os
import urllib2
import urllib
import pprint
import sys

# this is where my keys are kept hidden from Github
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
reload(sys)

# Knack response header:
# Content-Type application/json; charset=utf-8
# I guess from this that character encoding is UTF-8
sys.setdefaultencoding('utf-8')

import keys

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
    

with open('titles.txt', 'w') as titles:
    with open('descriptions.txt', 'w') as descriptions:
        for record in records:
            titles.write('%s\n' % record['field_5'].strip())
            descriptions.write('%s\n%s\n\n' % (record['field_5'].strip(), record['field_6'].strip()))
        

