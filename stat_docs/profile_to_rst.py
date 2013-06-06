import json
import os
from glob import glob

with open('fields.json') as f:
    fields = json.load(f)


def collect_group(name, profile_fields):
    res = []
    profile_fields.sort(key=lambda x: x['name'])
    res.append(name.capitalize())
    res.append("_" * len(name))

    for field in profile_fields:

        res.append('%s' % field['name'])
        res.append('+' * len(field['name']))
        res.append('\n  ``%s``\n' % field['help_text'])

        for key in ['required', 'max', 'min', 'default']:
            val = field.get(key, None)
            if val:
                res.append('\n  %s: %s' % (key, val))
        if field['choices']:
            res.append('\n  choices:')
            for choice in field['choices']:
                res.append('    - %s' % choice)
    return res


def profile_to_rst(name):
    with open(name) as f:
        profile = json.load(f)

    res = []
    name = os.path.basename(name)
    res.append(name)
    res.append("=" * len(name))


    profiles = {}

    for field in profile:
        field_template = fields[field['type']].copy()
        field_template.update(**field)
        profiles.setdefault(field_template.get("group", "fields"), []).append(field_template)

    for group in ["fields", "stats", "position", "models", "audio"]:
        group_val = profiles.pop(group, None)
        if group_val:
            res.extend(collect_group(group, group_val))

    # all other groups
    for key, val in profiles.items():
        res.extend(collect_group(key, val))



    return "\n".join(res)


if __name__ == '__main__':
    dirs = glob('profile/*.json')

    for x in dirs:
        res = profile_to_rst(x)
        name = os.path.basename(x.replace('json', 'rst'))
        #print name
        with open('docs/source/%s' % name, 'w') as f:
            f.write(res)



