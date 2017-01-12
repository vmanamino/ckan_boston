"""
This is a script to patch contact_point for a single dataset
I am testing a module knack_api_library
"""

import json, os
import pprint
from slugify import slugify
import sys
# this is where my keys are kept hidden from Github and this where my current modules are
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
from knack_api_library import get_knack_object

obj_id = raw_input("Please enter object id for the Knack record: ")

res = get_knack_object(obj_id)

data = json.loads(res.read())

print(data['field_147_raw'])
