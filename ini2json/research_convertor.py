from generic_convertor import generic_convertor


def handle_results(value):
    items = [x.strip('" ').split(":") for x in value.split(',') if value]
    for comps in items:
        component = comps[0]
        res = {}
        if component.isupper():
            res['weaponSubClass'] = component
        elif component in ['Cyborgs', 'Droids', 'Transport']:
            res['bodyClass'] = component
        elif component in ['Wall', 'Structure', 'Defense']:
            res['structureType'] = component
        elif component in ['RearmPoints', 'ProductionPoints', 'ResearchPoints', 'RepairPoints', 'Sensor', 'ECM',
                           'PowerPoints', 'Construct']:
            pass  # affects a global state
        else:  # forgot something...
            print 'Unknown filter: <%s>' % component
            exit(1)
        if len(comps) > 2:
            res[comps[1]] = int(comps[2])
        else:
            res[component] = int(comps[1])
        return res


def convert_research(ini, output_file, ids):
    handlers = {'results': handle_results,
                'techCode': int,
                'resultFunctions': None
                }
    generic_convertor(ini, output_file, ids, handlers=handlers)
