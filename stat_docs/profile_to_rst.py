import json
import os
from glob import glob




def _render(name, help_text, required, max_value, min_value, default, choices):
    res = ['- **%s.**' % name,
           '  %s\n' % help_text]

    for key, val in zip(['required', 'max', 'min', 'default'], [required, max_value, min_value, default]):
        if val:
            res.append('\n    %s: %s' % (key, val))
    if choices:
        res.append('\n    choices:')
        for choice in choices:
            res.append('      - %s' % choice)
    res.append('\n')
    return res


def render(field):
    return _render(field['name'], field['help_text'], field['required'], field['max'], field['min'], field['default'], field['choices'])


def render_key(field):
    help_text = "Key form :doc:`%s`" % field['reference']
    return _render(field['name'], help_text, field['required'], field['max'], field['min'], field['default'], field['choices'])


def render_key_list(field):
    help_text = "Coma separated keys rom :doc:`%s`" % field['reference']
    return _render(field['name'], help_text, field['required'], field['max'], field['min'], field['default'], field['choices'])


renders = {
    'key': render_key,
    'key_list': render_key_list,
    'default': render
}


with open('fields.json') as f:
    fields = json.load(f)


def collect_group(name, profile_fields):
    res = []
    profile_fields.sort(key=lambda x: x['name'])
    res.append(name.capitalize())
    res.append("_" * len(name))

    for field in profile_fields:
        if field['type'] in renders:
            render_function = renders[field['type']]
        else:
            render_function = renders['default']
        res.extend(render_function(field))



    return res


def profile_to_rst(name):
    with open(name) as f:
        profile = json.load(f)

    res = []
    name = os.path.basename(name)
    res.append(name.replace('.json', '.ini'))
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



