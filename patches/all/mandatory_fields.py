"""
This is a script to update conditionally
all datasets missing required metadata.
See the document mandataory_fields.
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


# first send request for list of packages
try:
    r = urllib2.urlopen('http://boston.ogopendata.com/api/3/action/package_list')
    print(r.code)
except urllib2.HTTPError as err:
    print(err.code)
    
data = json.loads(r.read())
titles = data['result']

# print(len(titles))

count = len(titles)
counter = 0

with open('ids.txt', 'w') as outfile:
    for title in titles:
        counter += 1
        outfile.write("%s\n" % title);

assert counter == count # prints to command line terminal if error

"""
Mandatory fields to be filled if empty
"""

contact_point = 'innovation'
contact_point_email = 'opengov@cityofboston.gov'
provider = 'innovation'

with open('report_mandatory_fields.txt', 'w') as first_report:
    first_report.write('dataset id\tresponse code\tcontact point\tcontact point email\tprovider\n')
    with open('patched_report.txt', 'w') as patch_report:
        patch_report.write('dataset id\tresponse code\tcontact point\tcontact point email\tprovider\n')
        with open('ids.txt') as ids:
            lines = ids.read().splitlines()
            if len(lines) == count:
                for line in lines:
                    payload = {'id': line}
                    data_string = urllib.quote(json.dumps(payload))
                    code = 0
                    
                    request = urllib2.Request(
                            'http://boston.ogopendata.com/api/3/action/package_show')
                    try:    
                        response = urllib2.urlopen(request, data_string)
                        code = response.code
                        data = json.loads(response.read())
                        id = data['result']['name']
                        first_report.write('%s\t%s' % (id,code))
                        """
                        patch payload, on condition
                        """
                        contact_empty = 0
                        contact_email_empty = 0
                        provider_empty = 0
                        # not sure if possible to have one, but not the other
                        # also not sure if possible to have key, but empty values
                        if(data['result'].has_key('contact_point') or data['result'].has_key('contact_point_email')):
                            # not sure if possible to have empty, null key
                            if not data['result']['contact_point']:
                                first_report.write('\tempty')
                                contact_empty = 1
                            else:
                                first_report.write('\t%s' % data['result']['contact_point'])
                            # not sure if possible to have empty, null key
                            if not data['result']['contact_point_email']:
                                first_report.write('\tempty')
                                contact_email_empty = 1
                            else:
                                first_report.write('\t%s' % data['result']['contact_point_email'])
                        # if any patch is needed for contact point or contact point email,
                        # this is the more likely case, no keys for either
                        else:
                            first_report.write('\tno key\tno key')
                            contact_empty = 1
                            contact_email_empty = 1
                        # not sure if possible to have provider key exist, but no value
                        if(data['result'].has_key('provider')):
                            if not data['result']['provider']:
                                first_report.write('\tempty')
                                provider_empty = 1
                            else:
                                first_report.write('\t%s' % data['result']['provider'])
                        # if patch is needed for provider, this is the more likely the case, no key
                        else:
                            first_report.write('\tno key')
                            provider_empty = 1
                        first_report.write('\n')    
                        if contact_empty or contact_email_empty or provider_empty:
                            # this is most likely the only case if a patch is to be made at all
                            # all this needs to be called from a library
                            if contact_empty and contact_email_empty and provider_empty:
                                payload = {'id': id, 'contact_point': contact_point, 
                                            'contact_point_email': contact_point_email, 'provider': provider}
                            if contact_empty and contact_email_empty and not provider_empty:
                                payload = {'id': id, 'contact_point': contact_point, 
                                            'contact_point_email': contact_point_email}
                            if contact_empty and not contact_email_empty and not provider_empty:
                                payload = {'id': id, 'contact_point': contact_point}
                            if contact_email_empty and not contact_empty and not provider_empty:
                                payload = {'id': id, 'contact_point_email': contact_point_email}
                            if provider_empty and contact_empty and not contact_email_empty:
                                payload = {'id': id, 'contact_point': contact_point, 'provider': provider}
                            if provider_empty and contact_email_empty and not contact_empty:
                                payload = {'id': id, 'contact_point_email': contact_point_email, 'provider': provider}
                            if provider_empty and not contact_empty and not contact_email_empty:
                                payload = {'id': id, 'provider': provider}
                            print('payload created')
                            print(payload)
                            
                            data_string = urllib.quote(json.dumps(payload))
                            request_patch = urllib2.Request(
                                'http://boston.ogopendata.com/api/3/action/package_patch')
                            request_patch.add_header('Authorization', key)
                            try:
                                response = urllib2.urlopen(request_patch, data_string)
                                patch_report.write('%s\t%s\n' % (id, response.code))
                                print('payload sent')
                                print(payload)
                            except urllib2.HTTPError as err:
                                patch_report.write('%s\t%s\n' % (id, err.code))
                                print(err.code)
                                print('payload not sent')
                                print(payload)
                        else:
                            patch_report.write('%s\tNA\n' % id)
                            print(str(id) + " is not being patched")
                    except urllib2.HTTPError as err:
                        first_report.write("%s\t%s\n" % (line, err.code))
                

