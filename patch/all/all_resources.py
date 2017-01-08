"""
This is a script to update all resources of all datasets.
Simply add or assign to the variable for the parameter to send
which corresponds to the appropriate metadata field.
See the Boston metadata scheme mapping to the CKAN
API parameters included in this repository.
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

# initial report of number of resources of each dataset, with code to help to confirm accuracy
with open('report_resources.txt', 'w') as report:
    
    # create headers of initial report
    report.write('dataset id\tnumber of resources\tcode\n')
    
    # ids or titles of datasets whose resources are to be patched. 
    with open('ids.txt') as ids:
        
        # report, next, of resources that were actually updated
        # noted lag in patching resource of Boston Open Budget - Project Phase Descriptions
        # specifically resource id 35368598-65f9-4a52-b5bf-95b242f84675
        # patch is requested successfully, but in get requests and on website
        # patch is not evident until several hours later.
        # such lag does not appear to me elsewhere
        with open('report_resources_updated.txt', 'w') as reported_updates:
            
            #create headers of next report of patched resources
            reported_updates.write('dataset id\tresources updated\n')
            
            #split each line at newline, effectively removing newline
            lines = ids.read().splitlines()
            
            # print(lines)
            # only if the count of lines from the text file is the same as the 
            # count of titles returned from the request above, proceed with patch
            if len(lines) == count:
                for line in lines:
                    print(line)
                    
                    # each new line start with code zero to be assigned later
                    # with actual response code
                    code = 0
                    
                    # payload to get the package, i.e. dataset
                    payload = {'id': line}
                    
                    # payload to json then to proper form to be carried in request
                    data_string = urllib.quote(json.dumps(payload))
                    
                    # prep request
                    request = urllib2.Request(
                        'http://boston.ogopendata.com/api/3/action/package_show')
                        
                    # convential exception handling
                    # only errors are written to initial report
                    # for each dataset that could not be got
                    try:    
                        response = urllib2.urlopen(request, data_string)
                        code = response.code
                    except urllib2.HTTPError as err:
                        
                        # write error to initial report
                        report.write("%s\tnull\t%s\n" % (line, err.code))
                    
                    # response assigned     
                    package_data = json.loads(response.read())
                    
                    # if package has a resource key, not necessarily values for resource properties
                    # then...
                    if package_data['result'].has_key('resources'):
                        
                        # number of resources dataset has
                        number = len(package_data['result']['resources'])
                        
                        # write to report
                        report.write("%s\t%s\t%s\n" % (line, number, code))
                        
                        # get each resource object
                        resources = package_data['result']['resources']
                        
                        # if in fact resource objects, 
                        # then...
                        if(len(resources)):
                            
                            # this is count of each resource patched
                            count = 0
                            
                            # go through each resource
                            for resource in resources:
                                
                                # identify resource to be patched
                                resource_to_update = resource['id']
                                print(resource_to_update)
                                
                                # create the payload, here the id and the parameter to be updated
                                resource_payload = {'id': resource_to_update, 'language':'en'}
                                
                                # format it to be carried in request
                                data_string = urllib.quote(json.dumps(resource_payload))
                                
                                # prep request
                                resource_request =  urllib2.Request(
                                            'http://boston.ogopendata.com/api/3/action/resource_patch')
                                
                                # add API key
                                resource_request.add_header('Authorization', key)
                                
                                # normal exception handling
                                try:
                                    response = urllib2.urlopen(resource_request, data_string)
                                    count += 1
                                except urllib2.HTTPError as err:
                                    print("resource not updated" + str(err.code))
                                    pass
                            
                            # write to report the dataset and count of resources patched    
                            # error will be noticed in count, which is not incremented
                            # count can be compared with initial report of number of resources
                            # of each dataset
                            reported_updates.write("%s\t%s\n" % (line, count))
                        else:
                            
                            # in case there no resources, this will be written
                            reported_updates.write("%s\tno resources\n" % (line))
                    else:
                        
                        # in case there is no key, this will be written
                        reported_updates.write("%s\tno key\n" % (line))
                        print(line + " has no resources key")
