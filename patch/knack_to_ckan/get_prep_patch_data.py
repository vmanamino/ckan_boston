# -*- coding: utf-8 -*- 

"""
Much of this was copied from ckan_boston/create/get_prep_data/get_prep_create_data.py
Essentially, I am switching out the package_create endpoint with package_patch.
I have to update the following (i.e. patch the datasets):
source - done
theme
btype - done
contact_name - done
tags - done

"""

import json, os
import pprint
from slugify import slugify
import sys
import time
import urllib2
import urllib
# this is where my keys are kept hidden from Github
sys.path.append('/home/ubuntu/workspace/code/ckan_boston')
import keys
reload(sys)

# CKAN API key
key = os.environ['CKAN_API_KEY'];

# Knack response header:
# Content-Type application/json; charset=utf-8
# I guess from this that character encoding is UTF-8
sys.setdefaultencoding('utf-8')

knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
knack_api_key= os.environ['KNACK_API_KEY']

# deal with empty values, currently understood as empty strings
# pass only the values in, not the key value pair
def value_none(val):
    value = ''
    if not val:
        value = 'none'
    else:
        value = val
    return value

# candidate for library...
# function to create multiple values in case relation of object to 
# dataset is 'many'.   Each value will be separated with pipe character.
def list_values(list_obj):
    count = len(list_obj)
    value_list = []
    
    # assumes that with first element empty, no values at all
    if count and list_obj[0]['identifier']:
        if count > 1:
            for obj in list_obj:
                value_list.append(str(obj['identifier']))
        else:
            value_list.append(str(list_obj[0]['identifier']))
        return_obj = value_list
    else:
        return_obj = "none"
    return return_obj

def date_formatted(time_obj):
    stamp = time_obj['unix_timestamp']
    temporal = time.strftime('%Y-%m-%d', time.gmtime(stamp/1000.))
    return temporal

def get_contact_info(obj):
    attributes = obj
    
    # contact is only one per dataset in our scheme, so can be confident in first place of all info
    contact_identifier = attributes[0]['id']
    
    # will have to prep request to add ID and KEY as headers
    url = 'https://api.knack.com/v1/objects/object_36/records/'+contact_identifier
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    response = json.loads(r.read())
    
    contact_info = get_gov_entity_info(response['field_216_raw'][0]['id'])
    
    # contact_info = json.loads(gov_entity_response.read())
    
    return contact_info
    
def get_gov_entity_info(identifier):
    url = 'https://api.knack.com/v1/objects/object_3/records/'+identifier
    
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    response = json.loads(r.read())
    
    info = []
    if response['field_12_raw']['email']:
        email = response['field_12_raw']['email']
        info.append(email)
    else:
        info.append('none')
    if response['field_13_raw']['formatted']:
        phone = response['field_13_raw']['formatted']
        info.append(phone)
    else:
        info.append('none')
        
    return info
    
def get_knack_data(page="1"):
    # both id and key are needed.  Id is for the specific application.
    # the key is to gain 'read' and 'write' permissions
    # knack_app_id = os.environ['KNACK_APPLICATION_ID']
    
    # knack_api_key= os.environ['KNACK_API_KEY']
    
    
    # data_string = urllib.quote(json.dumps(payload))
    
    # will have to prep request to add ID and KEY as headers
    url = 'https://api.knack.com/v1/objects/object_2/records?page='+page
    request = urllib2.Request(url)
                        
    request.add_header('X-Knack-Application-Id', knack_app_id)
    
    request.add_header('X-Knack-REST-API-Key', knack_api_key)
    
    try:
        r = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        r = err.code
    
    return r    
    
"""
functions to assign fixed values to parameters, later to be used in
building a library/module
"""

def classifications(label):
    value = ""
    if not label == "none" or label == "":
        label = label[0]
    if label == "Exempt Record":
        value = "exempt"
    elif label == "Public Record":
        value = "public"
    else:
        value = "exempt"
    return value

def frequencies(label):
    value = ""
    if not label == "none":
        label = label[0]
#     label: Continuously updated
#     value: R/PT1S
    if label == "Daily":
        value = "R/P1D"
#   - label: Three times a week
#     value: R/P0.33W
#   - label: Semiweekly
#     value: R/P3.5D
    elif label == "Weekly":
        value = "R/P1W"
#   - label: Three times a month
#     value: R/P0.33M
#   - label: Biweekly
#     value: R/P2W
#   - label: Semimonthly
#     value: R/P0.5M
    elif label == "Monthly":
        value = "R/P1M"
#   - label: Bimonthly
#     value: R/P2M
    elif label == "Quarterly":
        value = "R/P3M"
#   - label: Three times a year
#     value: R/P4M
#   - label: Semiannual
#     value: R/P6M
    elif label == "Annual":
        value = "R/P1Y"
    elif label == "Biennial":
        value = "R/P2Y"
#   - label: Triennial
#     value: R/P3Y
    else:
        value = "none"
    return value

# aka owner_org
def owner_orgs(label):
    value = ""
    if not label == "none":
        label = label[0]
    if label == "Department of Innovation and Technology" or label == "none":
        value = "data-cityofboston-gov"
    elif label == "Boston Water and Sewer Commission":
        value = "water-and-sewer-commission"
    else:
        value = "data-cityofboston-gov"
    # "environment-org",
    # "housing-authority",
    # "innovation-and-technology",
    # "transportation-org",
    
    return value

def open_values(label):
    value = "open"
    if label == "no" or label == "none":
        value = "closed"
    return value

def ckan_providers(label):
    value = ""
    # in case not a string, but a list is passed
    # only one provider in the Boston scheme
    if not type(label) == str:
        label = label[0]
    if label == "Administration & Finance":
        value = "finance"
    elif label == "Archives and Records Management":
        value = "archives"
    elif label == "Arts & Culture":
        value = "arts"
    elif label == "Assessing Department":
        value = "assessing"
    elif label == "Assistant Director of Operations, Consumer Affairs and Licensing":
        value = "consumer_asst"
    elif label == "Boston 311":
        value = "311"
    elif label == "Boston Centers for Youth and Families":
        value = "youth"
    elif label == "Boston EMS":
        value = "ems"
    elif label == "Boston Fire Department":
        value = "fire"
    elif label == "Boston Planning & Development Agency":
        value = "planning"
    elif label == "Boston Police Department":
        value = "police"
    elif label == "Boston Public Health Commission":
        value = "health_commission"
    elif label == "Boston Public Library":
        value = "library"
    elif label == "Boston Public Schools":
        value = "schools"
    elif label == "Boston Transportation Department":
        value = "transportation"
    elif label == "Boston Water and Sewer Commission":
        value = "water"
    elif label == "BPDA Management Information Systems":
        value == "bpda"
    elif label == "City Clerk":
        value = "clerk"
    elif label == "City of Boston Archaeology Program":
        value = "archaeology"
    elif label == "Civic engagement":
        value = "civic_engagement"
    elif label == "Consumer Affairs & Licensing Department":
        value = "consumer"
    elif label == "Data Literacy Librarian, Boston Open Data":
        value = "data_literacy"
    elif label == "Department of Innovation and Technology" or label == "none":
        value = "innovation"
    elif label == "Department of Neighborhood Development":
        value = "neighborhood_development"
    elif label == "Deputy Director, Real Estate Management and Sales":
        value = "real_estate"
    elif label == "Director of Publicity, Inspectional Services Department":
        value = "inspectional_publicity"
    elif label == "Director of Publicity, ISD":
        value = "publicity"
    elif label == "Director of Tax Policy & Communications":
        value = "tax_policy"
    elif label == "DoIT Data & Analytics":
        value = "doit_data"
    elif label == "Economic Development":
        value = "economic"
    elif label == "Education":
        value = "education"
    elif label == "Energy Manager, Environment Department":
        value = "energy_manager"
    elif label == "Environment, energy, and open space":
        value = "environment_energy"
    elif label == "Environment Department":
        value = "environment"
    elif label == "Fair Housing & Equity":
        value = "fair_housing"
    elif label == "GIS Team":
        value = "gis"
    elif label == "Health and human services":
        value = "health"
    elif label == "Housing & Neighborhood Development":
        value = "housing"
    elif label == "Information and Technology Cabinet":
        value = "it_cabinet"
    elif label == "Inspectional Services Department":
        value = "inspectional"
    elif label == "Intergovernmental Relations":
        value = "intergovernmental_relations"
    elif label == "Manager, DoIT GIS Team":
        value = "doit_gis"
    elif label == "Manager, Procurement Systems":
        value = "procurement"
    elif label == "Mayor's Office for Immigrant Advancement":
        value = "immigrant_advancement"
    elif label == "Mayor's Office of Emergency Management Services":
        value = "emergency_management"
    elif label == "Mayor":
        value = "mayor"
    elif label == "Neighborhood Services":
        value = "neighborhood"
    elif label == "Non-mayoral departments":
        value = "non_mayoral"
    elif label == "Office/Finance Manager, City of Boston Environment":
        value = "environment_manager"
    elif label == "Office of Arts & Culture":
        value = "arts_office"
    elif label == "Office of Budget Management":
        value = "budget"
    elif label == "Office of Economic Development":
        value = "economic_office"
    elif label == "Office of Human Resources":
        value = "hr"
    elif label == "Office of the Parking Clerk":
        value = "parking"
    elif label == "Operations":
        value = "operations"
    elif label == "Property Management":
        value = "property"
    elif label == "Public safety":
        value = "safety"
    elif label == "Purchasing Division":
        value = "purchasing"
    elif label == "Senior Systems and Network Operations Specialist, Boston Fire Department":
        value = "fire_operations"
    elif label == "Streets, transportation, and sanitation":
        value = "streets"
    elif label == "System Administrator, Office of Budget Management":
        value = "budget_admin"
    elif label == "Veterans Services":
        value = "veterans"
    else: # mandatory default
        value = "innovation"
    return value

def ckan_sources(label):
    value = ""
    if label == "Airport Statistics, Massport":
        value = "airport_statistics"
    elif label == "ArcGIS REST Services":
        value = "arcgis_rest"
    elif label == "Boston EMS electronic patient care report system":
        value = "ems_patient_care_report_system"
    elif label == "Boston Police Department Crime Statistics Feed":
        value = "police_crime_stats_feed"
    elif label == "Boston Public Library enterprise integrated library system (ILS)":
        value = "integrated_library_system"
    elif label == "Bostracks Enfocus":
        value = "bostracks_enfocus"
    elif label == "BPDA (Boston Planning & Development Agency) contract compliance database":
        value = "bpda_contract_compliance_db"
    elif label == "BRA pipeline database":
        value = "bra_pipeline_db"
    elif label == "City Clerk documents and assigned docket numbers":
        value ="city_clerk_documents"
    elif label == "City Constituent Relationship Management (CRM) System":
        value = "constituent_relationship_management_system"
    elif label == "City of Boston document management system":
        value = "document_management_system"
    elif label == "City of Boston Enterprise Resource Planning System, Financials":
        value = "resource_planning_system_financials"
    elif label == "City of Boston Enterprise Resource Planning System, Human Capital Management (HCM)":
        value = "resource_planning_system_human_capital"
    elif label == "City of Boston Voice over IP (VOIP) System":
        value = "voip_system"
    elif label == "City wide Budgeting and Forecasting Application":
        value = "budgeting_and_forecasting_app"
    elif label == "City wide Enterprise Energy Management System":
        value = "energy_management_system"
    elif label == "City wide Enterprise Permitting and Licensing Software":
        value = "permitting_and_licensing_software"
    elif label == "Computer aided dispatch system (CAD)":
        value = "computer_aided_dispatch_system"
    elif label == "Department of Neighborhood Development Data Server":
        value = "neighborhood_development_server"
    elif label == "ENERGY STAR Portfolio Manager®":
        value = "energy_star_portfolio_manager"
    elif label == "Internal":
        value = "internal"
    elif label == "IPS Data Management System (DMS)":
        value = "ips_data_management_system"
    elif label == "Labor Market Information, The Official Website of the Executive Office of Labor and Workforce Development (EOLWD)":
        value = "labor_market_info"
    elif label == "Massachusetts Artifact Tracking System":
        value = "massachusetts_artifact_tracking_system"
    else:
        value = "none"
    return value

def themes(entity):
    
    return

# aka spatial

def locations(entity):
    
    return

def btypes(label):
    value = ""
    if label == "Audio":
        value = "audio"
    elif label == "Image":
        value = "image"
    elif label == "Charts":
        value = "charts"
    elif label == "Map":
        value = "map"
    elif label == "Calendar":
        value = "calendar"
    elif label == "Forms":
        value = "forms"
    elif label == "External":
        value = "external"
    elif label == "Files and documents":
        value = "files_and_documents"
    elif label == "Tabular":
        value = "tabular"
    else:
        value = "none"
    return value

# """
# CKAN parameters
# """
#  # title_translated-en: "string" ; mandatory
# title_translated = ""

# # name: "slugged-title" ; required
# name = ""

# # btype: ["fixed values"]
# btype_list = []

# # notes_translated: {"en":"string"}
# notes_translated = ""

# # provider: "string" (fixed value) ; mandatory
# provider = ""

# # source: ["fixed values"]
# source = []

# # owner_org: "string" (fixed value); required 
# owner_org = ""

# # classification: "string" (fixed value)
# classification = ""

# # isopen: boolean true or false
# isopen = False

# # accrual_periodicity: "string" (fixed value)
# freq = ""

#  # temporal_from: "formatted date string"
# temp_from = ""
        
# # temporal_to: "formatted date string"
# temp_to = ""
        
# # temporal_notes: {"en": "string"}
# temp_notes = ""
        
# # theme: ["fixed values"]
# topic = []
        
# # location: ["fixed values"]
# geo = []
        
# # contact_point: "string" (fixed value)
# contact = "" # raw: string mandatory as contact_point
        
# # contact_point_email: "string" (email)
# email = "" # raw: string (email) mandatory as contact_point_email
        
# # contact_point_phone: "string" (phone number)
# phone = "" # raw string (phone number)

# # tags: ["string", "string"]
# tags = []

"""
start the work of getting Knack data
"""
response = get_knack_data()
data = json.loads(response.read())
pages = data['total_pages']

if pages > 1:
    
    # first page of records
    records = data['records']
    range_end_boundary = pages + 1
    
    # start on second page always
    for i in range(2, range_end_boundary):
        response = get_knack_data(str(i))
        data = json.loads(response.read())
        records += data['records']
    
else:
    records = data['records']

"""
assign knack data to variables/values for ckan parameters
"""

# count to limit number of CREATE calls to CKAN for testing
count = 0
with open('knack_metadata.txt', 'w') as knack:
    knack.write('title\ttype\tdesc\tprovider\tsource\tpublisher\tclassification'
    '\topen\tupdate freq\tfrom\tto\tcoverage notes\ttopic\tgeo coverage\tcontact point'
    '\tcontact email\tcontact phone\tkeywords\n')
    report = open('report_package_patch_tags.txt', 'w')
    report.write("These datasets have keywords to be added\n\n")
    report.write('id\tcode\tbtags\n')
    for record in records:
        count += 1
        """
        CKAN parameters
        """
         # title_translated-en: "string" ; mandatory
        title_translated = ""
        
        # name: "slugged-title" ; required
        name = ""
        
        # btype: ["fixed values"]
        btype_list = []
        
        # notes_translated: {"en":"string"}
        notes_translated = ""
        
        # provider: "string" (fixed value) ; mandatory
        provider = ""
        
        # source: ["fixed values"]
        sources = []
        
        # owner_org: "string" (fixed value); required 
        owner_org = ""
        
        # classification: "string" (fixed value)
        classification = ""
        
        # isopen: boolean true or false
        isopen = ""
        
        # accrual_periodicity: "string" (fixed value)
        freq = ""
        
         # temporal_from: "formatted date string"
        temp_from = ""
                
        # temporal_to: "formatted date string"
        temp_to = ""
                
        # temporal_notes: {"en": "string"}
        temporal_notes = ""
                
        # theme: ["fixed values"]
        topic = []
                
        # location: ["fixed values"]
        geo = []
                
        # contact_point: "string" (fixed value)
        contact_point = "" # raw: string mandatory as contact_point
                
        # contact_point_email: "string" (email)
        contact_point_email = "" # raw: string (email) mandatory as contact_point_email
                
        # contact_point_phone: "string" (phone number)
        contact_point_phone = "" # raw string (phone number)
        
        # tags: [{"name": "value"}, {"name": "value"}]
        tag_dict = {}
        tags = []

        title = record['field_5_raw'].strip()
        print(title)
        # param
        title_translated = title
        
        #param
        name = slugify(title)
        # print(name)
        dataset_types = list_values(record['field_152_raw'])
        
        # call the types function above
        for dtype in dataset_types:
            btype = btypes(dtype)
            
            #param
            btype_list.append(btype)
        # print(btype_list)    
        # print(btype_list)
        # description assigned but not written because of hidden characters which 
        # interrupt formatting for report
        # desc =  record['field_6_raw'].strip()
        # Description to large in most cases to include in file.
        # Instead include object reference.  Together with field (field_6), can easily query
        # for description to create notes parameter.
        desc = record['id']
        
        # param
        notes_translated = record['field_6_raw'].strip()
        
        # param, Knack metadata
        knack_provider = list_values(record['field_186_raw'])
        # print(knack_provider)
        # knack_provider = knack_provider[0]
        provider = ckan_providers(knack_provider)
        # print('this is the provider')
        # print(provider)
        
        # skip sources until configuration uptodate
        knack_sources = list_values(record['field_164_raw'])
        # print('knack sources')
        # print(knack_sources)
        if not knack_sources == "none":
            for source in knack_sources:
                ckan_source = ckan_sources(source)
                
                # param, skip for now until configuration list is updated
                sources.append(ckan_source)
        else:
            sources.append("none")
        # print(sources)    
        publisher = list_values(record['field_205_raw'])
        owner_org = owner_orgs(publisher)
        # print(owner_org)
        classification = list_values(record['field_155_raw'])
        classification = classifications(classification)
        # print(classification)
        open_value = record['field_308_raw']
        open_value =  value_none(open_value)
        isopen = open_values(open_value)
        # print(isopen)
        freq = list_values(record['field_139_raw'])
        freq = frequencies(freq)
        # print(freq)
        
        """
        dealing with date info
        """
        if record['field_121_raw']:
            temp_from = date_formatted(record['field_121_raw'])
        else:
            temp_from = 'none'
        if record['field_122_raw']:
            temp_to = date_formatted(record['field_122_raw'])
        else:
            temp_to = 'none'
        
        temporal_notes = record['field_159_raw'].strip()
        temporal_notes = value_none(temporal_notes)
        
        # skip in CREATE call
        topics = list_values(record['field_146_raw'])
        # skip in CREATE call
        location = list_values(record['field_136_raw'])
        # skip in CREATE call
        keywords = list_values(record['field_321_raw'])
        # print(keywords)
        # create dict to be element of a list, which is the value of tags param
        # each tag must contain only alphanumeric, dash or 'space' or underscore, otherwise 409
        if not keywords == "none":
            for word in keywords:
                tag_dict = {}
                tag_dict['name'] = word
                tags.append(tag_dict)
        # print(tags)
        """
        Get contact info.  Was not able to get Knack filter to work.
        Display name for Gov Entity (Object 3) which is the parent of Contact is
        the Title, which is appropriate for two reasons.  1: Labels can be many and for different
        purposes, the title is single and authoritative.  The value must be unique.
        2: Since Title is Display Name and unique, it can be queried on from the value supplied to Dataset (Object 2),
        and any changes to the Title will cascade to the Contact (Object 36), 
        and in turn to Dataset (Object 2)
        """
        # there is only one contact per dataset, so can be confident of first place in list
        
        contact_name = ''
        contact_info_list = []
        
        if record.has_key('field_147'):
            if (record['field_147']):
                contact_name = record['field_147_raw'][0]['identifier'].strip()
                # print(contact_name)
                try:
                    contact_info_list = get_contact_info(record['field_147_raw'])
                    
                except:
                    e = sys.exc_info()[0]
                    contact_info_list = ['none', 'none']
                    # print(e)
            else:
                # print(record['field_5']+' has no contact')
                contact_name = 'none'
                contact_info_list = ['none', 'none']
        else:
            # print(record['field_5'] + 'has no contact field key')
            contact_name = 'none'
            contact_info_list = ['none', 'none']
        
        knack.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}"
            "\t{14}\t{15}\t{16}\t{17}\n".format(
            title, dataset_types, desc, knack_provider, knack_sources, publisher, classification, open_value,
            freq, temp_from, temp_to, temporal_notes, topics, location, contact_name, contact_info_list[0],
            contact_info_list[1], keywords))
            
        """
        Here create Payload
        """
        # case 1, no source if not source[0] == "none":
        # include source: list parameter
        
        contact_point = ckan_providers(str(contact_name))
        """
        update contact_point and sources
        """
        # if not contact_point:
        #     contact_point = "innovation"
            
        # if not sources[0] == "none":
        
        #     # name doubles as id for patching, updating
        #     payload = {"id": name, "source": sources, "contact_point": contact_point}
        # else:
        #     payload = {"id": name, "contact_point": contact_point}
        
        """
        update btype
        """
        # if len(btype_list) and not btype_list[0] == "none":
        #     payload = {"id": name, "btype": btype_list}
            
        #     """
        #     Here make your CKAN CREATE call
        #     """
        #     data_string = urllib.quote(json.dumps(payload))
        #     request = urllib2.Request(
        #                 'http://boston.ogopendata.com/api/3/action/package_patch')
        #     # add Authorization header
        #     request.add_header('Authorization', key)
        #     # make request
        #     try:
        #         response = urllib2.urlopen(request, data_string)
        #         report.write('%s\t%s\t%s\n' % (name, response.code, btype_list))
        #         print(response)
        #     except urllib2.HTTPError as err:
        #         report.write('%s\t%s\t%s\n' % (name, response.code, btype_list))
        #         print(err)   
        """
        update tags
        """
        if len(tags):
            print(tags)
            payload = {"id": name, "tags":tags}
            data_string = urllib.quote(json.dumps(payload))
            request = urllib2.Request(
                    'http://boston.ogopendata.com/api/3/action/package_patch')
            # add Authorization header
            request.add_header('Authorization', key)
            try:
                response = urllib2.urlopen(request, data_string)
                report.write('%s\t%s\t%s\n' % (name, response.code, tags))
                print(response)
            except urllib2.HTTPError as err:
                report.write('%s\t%s\t%s\n' % (name, err.code, tags))
                print(err)    
                
        # data_string = urllib.quote(json.dumps(payload))
        # request = urllib2.Request(
        #             'http://boston.ogopendata.com/api/3/action/package_patch')
        # # add Authorization header
        # request.add_header('Authorization', key)
        # make request
        # try:
        #     response = urllib2.urlopen(request, data_string)
        #     report.write('%s\t%s\t%s\n' % (name, response.code, contact_point))
        #     print(response)
        # except urllib2.HTTPError as err:
        #     report.write('%s\t%s\t%s\n' % (name, response.code, contact_point))
        #     print(err)               
        
               
            
            
        
