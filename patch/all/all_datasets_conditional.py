"""This is a script to patch all datasets on Boston Open Data Hub
Simply add or assign to the variable for the parameter to send
which corresponds to the appropriate metadata field.
See the Boston metadata scheme mapping to the CKAN
API parameters included in this repository
I will revise all this, isolate tasks, and create a library
for CKAN metadata editing via the API
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

"""
create a list of all 
Boston Open Data Hub datasets to be patched
"""

# first send request for list of packages
# package_list does not show packages in draft
r = urllib2.urlopen('http://boston.ogopendata.com/api/3/action/package_list')

# check if response is success, error will display in command line terminal
print(r.code)
assert r.code == 200

data = json.loads(r.read())
titles = data['result']

# check that length of response result is number of titles you write to file
count = len(titles)
counter = 0

# id is the parameter of which each title will be a value
with open('ids.txt', 'w') as outfile:
    for title in titles:
        counter += 1
        outfile.write("%s\n" % title);
        
# test count of ids against count of titles
assert counter == count # currently 135, 5 of these are blocked from public view

"""
parameter 
to be updated, i.e. patching the dataset
"""

# Boston Open Data Hub license for ALL datasets
cob_license_id = 'odc-pddl'

# Boston Open Data Hub language parameter, supply appropriate language code


# # check that request for missing dataset id, fails
# missing_dataset_id = 'this-dataset-not-there'

# write report with title/id and http code
with open('report_datasets_patched_conditional.txt', 'w') as report:
    # report.write('dataset id\thttp response\contact_point\tcontact_email\n')
    # read ids from ids.txt, but test with ids.1.txt first
    with open('ids.txt') as ids:
        #split each line at newline, effectively removing newline
        lines = ids.read().splitlines()
        # only if the count of lines from the text file is the same as the 
        # count of titles returned from the request above, proceed with patch
        if len(lines) == count:
            for line in lines:
                print(line)
                
                # payload = {"id": line, "license_id": cob_license_id}
                # data_string = urllib.quote(json.dumps(payload))
                
                # # prep request
                # request = urllib2.Request(
                #     'http://boston.ogopendata.com/api/3/action/package_patch')
    
                # add Authorization header
                # request.add_header('Authorization', key)
                
                ## make request
                # try:
                #     response = urllib2.urlopen(request, data_string)
                #     report.write("%s\t%s\n" % (line, response.code))
                # except urllib2.HTTPError as err:
                #     report.write("%s\t%s\n" % (line, err.code))
            
