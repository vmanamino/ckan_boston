"""
This is a script to help create dataset ids 
in preparation to patch a parameter on a subset of 
datasets on Boston Open Data Hub.

The example made here is of creating a tag for datasets
that were migrated from the old open data portal, and which
will no longer be maintained.  Those datasets will be tagged
with legacy portal for quick identification and retrieval.

The CKAN API does not seem to able to add directly to the tags list
of a dataset.  The patch request to a dataset will replace the tags list
with your tags parameter: tags [{name: new tag}] The solution is to append to the
current tags list which can be got via package_show.  Append to the list returned
then create a patch of the 'new' tags list, which has both the current tags and
the one you want to add.
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

with open('/home/ubuntu/workspace/code/ckan_boston/patches/subset/nonalphanum/dataset_ids.txt') as ids:
    
    # initial report to check accuracy of ids and discover and note correct ones
    with open('dataset_ids_report.txt', 'w') as initial_report:
        initial_report.write('formatted id\tresponse\tcorrect id\n')
        lines = ids.read().splitlines()
        for line in lines:
            payload = {'id': line}
           
            data_string = urllib.quote(json.dumps(payload))
            
            package_request =  urllib2.Request(
                            'http://boston.ogopendata.com/api/3/action/package_show')
           
            # add API key in case of private datasets needing to be patched
            package_request.add_header('Authorization', key)
            
            try:
                response = urllib2.urlopen(package_request, data_string)
                initial_report.write('%s\t%s\tcorrect\n' % (line, response.code))
            except urllib2.HTTPError as err:
                initial_report.write('%s\t%s\tincorrect\n' % (line, err.code))


