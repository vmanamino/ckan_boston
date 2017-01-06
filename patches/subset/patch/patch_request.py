"""
This script sends the patch to replace the tags list.
Replacing the tags list is the only way, it seems, to add a tag.
First, we need to obtain the correct dataset id, so run
the datasets.py script in this directory (ckan_boston/patches/subset/patch)
Correct ids where noted in dataset_ids_report.txt file.

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
with open('dataset_ids_report.txt') as ids:
    with open('dataset_to_patch_package_request.txt', 'w') as package_to_patch:
        package_to_patch.write('dataset id\tcode\tcomment\n')
        with open('dataset_patched.txt', 'w') as report:
            report.write('dataset\tcomment/code\n')
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
                    # print(dataset_id)
                    payload = {'id': dataset_id}
                   
                    data_string = urllib.quote(json.dumps(payload))
                    
                    package_request =  urllib2.Request(
                                    'http://boston.ogopendata.com/api/3/action/package_show')
                   
                    # add API key
                    package_request.add_header('Authorization', key)
                    
                    try:
                        response = urllib2.urlopen(package_request, data_string)
                        package_to_patch.write('%s\t%s\tcorrect id\n' % (dataset_id, response.code))
                        
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
                                # this datasset has legacy portal tag, go no further
                                print('this dataset has tag legacy portal')
                                legacy = 1
                                break
                        if not legacy:
                            # this dataset does not have the tag: needs to be patched
                            print('end of tags, this dataset does not have legacy portal tag')
                            tags.append({'name':'legacy portal'})
                            payload_id = id
                            payload_tags = tags
                            payload = {'id': id, 'tags': tags}
                            data_string = urllib.quote(json.dumps(payload))
                            
                            # prep request
                            request = urllib2.Request(
                                    'http://boston.ogopendata.com/api/3/action/package_patch')
        
                            # add Authorization header
                            request.add_header('Authorization', key)
                            
                            try:
                                response = urllib2.urlopen(request, data_string)
                                report.write("%s\t%s\n" % (line, response.code))
                            except urllib2.HTTPError as err:
                                report.write("%s\t%s\n" % (line, err.code))
                            # print(tags)
                            
                        else:
                            report.write('%s\thad/has tag\n' % (line))
                        
                    except urllib2.HTTPError as err:
                        print('This dataset had the wrong id for request' + dataset_id)
                        package_to_patch.write('%s\t%s\tincorrect id\n' % (dataset_id, err.code))
                header += 1
        