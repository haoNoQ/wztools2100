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

    def get_header(self):
        result = [";Section headers in brackets [...] is system ID of %s items. This IDs should be unique." % self.file_name,
                  ';Following properties can be used in %s items:' % self.file_name]

        fields = self.keys()
        fields.sort(key=lambda x: self.field_order.index(x))
        lines = [self._get_field_header_line(key) for key in fields]

        len_name = max([len(x[0]) for x in lines])
        #len_type = min(max([len(x[1]) for x in lines]), 40)

        template = ';  %-{0}s   %s'.format(len_name)

        result += (template % x for x in lines)
        return '\n'.join(result)

    def _get_field_value_type(self, item):
        convert_to = item['convert_to']
        item_type = item['type']
        if item_type == 'choice':
            return 'one of: %s' % '|'.join([str(x) for x in item['choices']])
        if convert_to == 'string_list':
            return 'comma-separated string list'
        if convert_to == 'boolean':
            return '1 - True,  2 - False'
        if convert_to == 'pie':
            return 'comma-separated pie file names'
        if convert_to == 'int':
            return 'integer'
        if convert_to == "str":
            return 'string'
        return convert_to

    def _get_field_header_line(self, key):
        item = self[key]
        value_type = '<%s>' % self._get_field_value_type(item)
        return item['name'], value_type


def get_profiles_name_list():
    return [name[:-5] for name in os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]


def get_profiles():
    return [Profile(name[:-5]) for name in os.listdir(os.path.join(this_dir, '../ini_tools/profile')) if name.endswith('.json')]