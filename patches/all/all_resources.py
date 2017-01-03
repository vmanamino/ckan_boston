"""
This is a script to update all resources of all datasets.
Simply add or assign to the variable for the parameter to send
which corresponds to the appropriate metadata field.
See the Boston metadata scheme mapping to the CKAN
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

"""
create a list of all 
Boston Open Data Hub datasets to be patched
"""

# first send request for list of packages
r = urllib2.urlopen('http://boston.ogopendata.com/api/3/action/package_list')

# check if response is success, error will display in command line terminal
# print(r.code)
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
parameter in resource to be updated, i.e. patch
"""
language = 'en'

with open('report_resources.txt', 'w') as report:
    report.write('dataset id\tnumber of resources\tcode\n')
    with open('ids.txt') as ids:
        with open('report_resources_updated', 'w') as reported_updates:
            reported_updates.write('dataset id\tresources updated\n')
            #split each line at newline, effectively removing newline
            lines = ids.read().splitlines()
            # print(lines)
            # only if the count of lines from the text file is the same as the 
            # count of titles returned from the request above, proceed with patch
            if len(lines) == count:
                for line in lines:
                    print(line)
                    code = 0
                    payload = {'id': line}
                    data_string = urllib.quote(json.dumps(payload))
                    
                    # prep request
                    request = urllib2.Request(
                        'http://boston.ogopendata.com/api/3/action/package_show')
                    try:    
                        response = urllib2.urlopen(request, data_string)
                        code = response.code
                    except urllib2.HTTPError as err:
                        report.write("%s\tnull\t%s\n" % (line, err.code))
                        
                    package_data = json.loads(response.read())
                    if package_data['result'].has_key('resources'):
                        number = len(package_data['result']['resources'])
                        report.write("%s\t%s\t%s\n" % (line, number, code))
                        resources = package_data['result']['resources']
                        if(len(resources)):
                            count = 0
                            for resource in resources:
                                resource_to_update = resource['id']
                                print(resource_to_update)
                                resource_payload = {'id': resource_to_update, 'language':'en'}
                                data_string = urllib.quote(json.dumps(resource_payload))
                                
                                # prep request
                                resource_request =  urllib2.Request(
                                            'http://boston.ogopendata.com/api/3/action/resource_patch')
                                
                                # add key
                                resource_request.add_header('Authorization', key)
                                
                                try:
                                    response = urllib2.urlopen(resource_request, data_string)
                                    count += 1
                                except urllib2.HTTPError as err:
                                    print("resource not updated" + str(err.code))
                                    pass
                            reported_updates.write("%s\t%s\n" % (line, count))
                        else:
                            reported_updates.write("%s\t0\n" % (line))
                    else:
                        reported_updates.write("%s\t0\n" % (line))
                        print(line + " has no resources key")
