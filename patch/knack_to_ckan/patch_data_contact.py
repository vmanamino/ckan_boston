"""
This is a script to patch contact_point for a single dataset
I am testing a module knack_api_library
"""

import json, os
import pprint
from slugify import slugify
import sys
import urllib2
import urllib
import keys

# this is where my keys are kept hidden from Github
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
reload(sys)

# CKAN API key
key = os.environ['CKAN_API_KEY'];

# Knack response header:
# Content-Type application/json; charset=utf-8
# I guess from this that character encoding is UTF-8
sys.setdefaultencoding('utf-8')

knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
knack_api_key= os.environ['KNACK_API_KEY']

print(key)