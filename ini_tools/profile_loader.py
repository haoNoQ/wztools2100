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


def get_profiles_name_list():
    return [name[:-5] for name in os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]


def get_profiles():
    return [Profile(name[:-5]) for name in
            os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]