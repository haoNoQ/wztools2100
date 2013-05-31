import json
import os
from glob import glob

with open('fields.json') as f:
    fields = json.load(f)


def profile_to_rst(name):
    with open(name) as f:
        profile = json.load(f)

    res = []

    name = os.path.basename(name)
    res.append(name)
    res.append("=" * len(name))

    profile.sort(key=lambda x: x['name'])

    for field_dict in profile:
        field = fields[field_dict['type']]
        field.update(field_dict)  # update data with defaultt values
        res.append('%s' % field['name'])
        res.append('-' * len(field['name']))
        res.append('\n  ``%s``\n' % field['help_text'])

        for key in ['required', 'max', 'min', 'default']:
            val = field.get(key, None)
            if val:
                res.append('\n  %s: %s' % (key, val))
        if field['choices']:
            res.append('\n  choices:')
            for choice in field['choices']:
                res.append('    - %s' % choice)
    return "\n".join(res)


if __name__ == '__main__':
    dirs = glob('profile/*.json')

    for x in dirs:
        res = profile_to_rst(x)
        name = os.path.basename(x.replace('json', 'rst'))
        #print name
        with open('docs/source/%s' % name, 'w') as f:
            f.write(res)



