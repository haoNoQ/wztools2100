from __future__ import print_function
from .profile_loader import get_profiles

MAX_ITEM_TYPE_LENGTH = 40


def get_header(profile):
    result = [
        "; Section headers in brackets [...] is system ID of %s items. This IDs should be unique." % profile.file_name,
        ]
    lines = []
    for key, item in sorted(profile.items(), key=lambda x: profile.field_order.index(x[0])):
        convert_to = item['convert_to']
        item_type = item['type']
        help_text = item.get('help_text', 'unknown!!!')
        name = item['name']

        value_type = item_type

        if item.get('choices'):
            text = '|'.join(str(x) for x in item['choices'])
            if len(text) < MAX_ITEM_TYPE_LENGTH - 2:
                value_type = text
            else:
                help_text += ' [%s]' % ', '.join([str(x) for x in item['choices']])
        elif item_type == 'key':
            value_type = 'ID for %s' % item['reference']
        elif item_type == 'key_list':
            value_type = 'comma-separated list of %s IDs' % item['reference']
        elif convert_to == 'string_list':
            value_type = 'comma-separated list'
        elif convert_to == 'pie':
            value_type = 'comma-separated pies'
        elif convert_to == 'int':
            value_type = 'integer'
        elif convert_to == "str":
            value_type = 'string'

        value_type = '<%s>' % value_type
        lines.append((name, value_type, help_text))

    len_name = max([len(x[0]) for x in lines])
    len_type = min(max([len(x[1]) for x in lines]), MAX_ITEM_TYPE_LENGTH)

    template = ';  %-{0}s   %-{1}s  %s'.format(len_name, len_type)

    result += (template % x for x in lines)
    return '\n'.join(result)

if __name__ == "__main__":
    for profile in get_profiles():
        print("\n" * 3)
        print(get_header(profile))