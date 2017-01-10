"""
Could not get the Knack API filter to work
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

url = 'https://api.knack.com/v1/objects/object_2/records'

# filters = [
#   {
#     "field":"field_285_raw",
#     "operator":"is",
#     "value":"Director of Publicity, ISD"
#   }
# ]

# data_string = json.dumps(filters)
# url += '?filters=' + urllib.quote(data_string.encode("utf-8"))

filters = urllib.quote_plus("[{\"field\":\"field_285\",\"operator\":\"is\",\"value\":\"Director of Publicity, ISD\"}]")

url = url + '?filters=' + filters

print(url)
request = urllib2.Request(url)

request.get_method = lambda: 'GET'
                        
request.add_header('X-Knack-Application-Id', knack_app_id)
    
request.add_header('X-Knack-REST-API-Key', knack_api_key)

f = None

try:
    f = urllib2.urlopen(request)
except urllib2.HTTPError, ex:
    if ex.fp:
        extra = ex.fp.read()
        print "Knack Error: %s" % extra
    else:
        raise
data = json.loads(f.read())
 
print data