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
        with open(os.path.join(this_dir, 'fields.json')) as f:
            fields = json.load(f)

        with open(os.path.join(this_dir, 'profile', '%s.json' % file_name)) as f:
            data = json.load(f)

        for field in data:
            field_type = field['type']
            profile = fields[field_type].copy()
            profile.update(**field)
            self[field['name']] = profile


def get_profiles_name_list():
    return [name[:-5] for name in os.listdir(os.path.join(this_dir, 'profile')) if name.endswith('.json')]
