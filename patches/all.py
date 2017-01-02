"""This is a script to patch all datasets on Boston Open Data Hub
Simply add or assign to the variable for the parameter to send
which corresponds to the appropriate metadata field.
See the Boston metadata scheme mapping to the CKAN_API_KEY
API parameters included in this repository
"""

import json, os
import urllib2
import urllib
import pprint
import sys
# this is where my keys are kept hidden from Github
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
import keys
# using environment variable to keep actual key hidden from Github
key = os.environ['CKAN_API_KEY'];

# create a list of all Boston Open Data Hub datasets to be patched

# first send request for list of packages
r = urllib2.urlopen('http://boston.ogopendata.com/api/3/action/package_list')

# check if response is success, error will display in command line terminal
assert r.code == 200

# check that length of response result is number of titles you write to file
data = json.loads(r.read())
titles = data['result']
count = len(titles)
counter = 0
# id is the parameter of which each title will be a value
with open('ids.txt', 'w') as outfile:
    for title in titles:
        counter += 1
        outfile.write("%s\n" % title);
# test count of ids against count of titles
assert counter == count # currently 135, 5 of these are blocked from public view






