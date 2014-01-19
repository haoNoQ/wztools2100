import json


def generic_convertor(ini, output_file, ids, handlers=None):
    profile = ini.get_profile_for_ini()
    _handlers = profile.get_deafult_handlers()
    if handlers:
        _handlers.update(handlers)
    data = {}

    def handle_value(field, value):
        handler = _handlers.get(field)
        if not handler:
            print "Cant find handler of %s" % field
            return None
        res = handler(value.strip('" '))
        if profile[field]['type'] == 'key_list':
            return [ids.get(x, x) for x in res]
        if profile[field]['type'] == 'key':
            return ids.get(value, value)
        return res

    for section, section_fields in ini.items():
        entry = {}
        for field, value in section_fields.items():
            result = handle_value(field, value)
            if result:
                entry[field] = result
        name = entry.pop('name', 'name')
        entry['id'] = section  # for backwards compatibility
        data[name] = entry

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, separators=(',', ': '), sort_keys=True)