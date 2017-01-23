import json
from knack_api_library import get_knack_dataset, get_contact_object
import time

class KnackObject:
    
    # get all objects in json for easy assignment
    # using static methods because not using or assigning anything to properties
    # of the class
    @staticmethod
    def get_in_json(ident):
        res = get_knack_dataset(ident)
        return json.loads(res.read())
        
    # function to create multiple values in case relation of object to 
    # dataset is 'many'.
    @staticmethod
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
        
    # add function to separate list values with pipe
    @staticmethod
    def list_values_display(list_obj):
        return '|'.join(list_obj)
        
    @staticmethod
    def value_none(val):
        value = ''
        if not val:
            value = 'none'
        else:
            value = val
        return value
        
class KnackDatasets:
    pass


class KnackDataset(KnackObject):
    datasets = 0
    def __init__(self, ident):
        self.ident = ident
        self.json = self.get_in_json(ident)
        self.title = self.json['field_5_raw'].strip()
        self.types = self.list_values(self.json['field_152_raw'])
        self.desc = self.json['field_6_raw']
        self.prov = self.list_values(self.json['field_186_raw'])
        self.sources = self.list_values(self.json['field_164_raw'])
        self.pub = self.list_values(self.json['field_205_raw'])
        self.classif = self.list_values(self.json['field_155_raw'])
        self.open_status = self.value_none(self.json['field_308_raw'])
        self.freq = self.list_values(self.json['field_139_raw'])
        self.time_from = self.get_date_str(self.json['field_121_raw'])
        self.time_to = self.get_date_str(self.json['field_122_raw'])
        self.time_notes = self.value_none(self.json['field_159_raw'])
        self.topics = self.list_values(self.json['field_146_raw'])
        self.location = self.list_values(self.json['field_136_raw'])
        self.keywords = self.list_values(self.json['field_321_raw'])
        KnackDataset.datasets += 1
        
    def get_date_str(self, time_obj):
        if time_obj:
            stamp = time_obj['unix_timestamp']
            return time.strftime('%Y-%m-%d', time.gmtime(stamp/1000.)) 
        else:
            return 'none'
        
        
dataset = KnackDataset('57b21c8e67d437161a265671')
print(dataset.list_values_display(dataset.keywords))
print(KnackDataset.datasets)
# print(dataset.title)
# print(dataset.types)
# print('types separated')
# print(dataset.list_values_piped(dataset.types))
# print(help(KnackDataset))