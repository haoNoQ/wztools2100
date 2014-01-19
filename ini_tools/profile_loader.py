import os
import json

this_dir = os.path.dirname(__file__)


def string_list(val):
    return [item.strip() for item in val.split(',') if item.strip()]


def boolean(val):
    return val == "1"


class Profile(dict):
    """
    Convert profile json files to dict with params
    """
    COMPONENTS = ['brain', 'ecm', 'repair', 'sensor', 'weapons', 'body', 'propulsion', 'construction']
    HANDLERS = {
        'string_list': string_list,
        'int': int,
        'bool': int,
        'str': str
    }

    def get_deafult_handlers(self):
        handlers = {}
        for field, field_info in self.items():
            handlers[field] = self.HANDLERS[field_info['convert_to']]
        return handlers

    def __init__(self, file_name):
        self.file_name = file_name
        with open(os.path.join(this_dir, '../ini_tools/fields.json')) as f:
            fields = json.load(f)

        with open(os.path.join(this_dir, '../ini_tools/profile', '%s.json' % file_name)) as f:
            data = json.load(f)

        self.field_order = []

        for field in data:
            self.field_order.append(field['name'])
            field_type = field['type']
            profile = fields[field_type].copy()
            profile.update(**field)
            self[field['name']] = profile

    def get_reference_keys(self, field_name):
        field = self[field_name]
        assert 'reference' in field, "%s field '%s' has missed reference" % (self.file_name, field_name)
        reference = field['reference']
        items = reference.split('|')
        result_keys = []
        for item in items:
            if item == 'component':
                result_keys.extend(self.COMPONENTS)
            else:
                result_keys.append(item)
        return result_keys




def get_profiles_name_list():
    return [name[:-5] for name in os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]


def get_profiles():
    return [Profile(name[:-5]) for name in
            os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]