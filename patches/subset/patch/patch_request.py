"""
This script sends the patch to replace the tags list.This
Replacing the tags list is the only way, it seems, to add a tag.
First, we need to obtain the correct dataset id
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
here get the id for the patch request
"""
with open('dataset_ids_report.1.txt') as ids:
    with open('dataset_to_patch_package_request.txt', 'w') as package_to_patch:
        package_to_patch.write('dataset id\tcode\tcomment\n')
        lines = ids.read().splitlines()
        header = 0
        for line in lines:
            # each line, determine id
            dataset_id = ''
            if header:
                line, code, id = line.split('\t')
                if code == '200':
                    dataset_id = line
                else:
                    dataset_id = id
                
                ## get the dataset to be patched
                
                payload = {'id': dataset_id}
               
                data_string = urllib.quote(json.dumps(payload))
                
                package_request =  urllib2.Request(
                                'http://boston.ogopendata.com/api/3/action/package_show')
               
                # add API key
                package_request.add_header('Authorization', key)
                
                try:
                    response = urllib2.urlopen(package_request, data_string)
                    package_to_patch.write('%s\t%s\tcorrect\n' % (dataset_id, response.code))
                    
                    package_data = json.loads(response.read())
                    
                    # id for patch request
                    id = package_data['result']['name']
                    
                    # list of tags 
                    tags = package_data['result']['tags']
                    
                    print(id)
                    for tag in tags:
                        legacy = 0
                        print(tag['name'])
                        if tag['name'] == 'legacy portal':
                            print('has legacy portal tag')
                            legacy = 1
                            break
                    if not legacy:
                        print('this dataset does not have the tag')
                    else:
                        print('this dataset does have tag')
                    
                except urllib2.HTTPError as err:
                    package_to_patch.write('%s\t%s\tincorrect\n' % (dataset_id, err.code))
            header += 1
        