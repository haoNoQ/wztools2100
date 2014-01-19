import os
from glob import glob
from research_convertor import convert_research
from ini_tools.ini_file import IniFile
from generic_convertor import generic_convertor


INPUT_PATH = 'G:/warzone2100/data'
OUTPUT_PATH = 'G:/projects/wztools2100/base/stats/json'

if __name__ == '__main__':
    BASE_PATH = os.path.join(INPUT_PATH, 'base', 'stats')

    base_files = glob('%s/*.ini' % BASE_PATH)
    base_inis = {os.path.basename(x)[:-4]: IniFile(x) for x in base_files}

    ids = {}
    for ini in base_inis.values():
        ids.update({k: v['name'].strip('" ') for k, v in ini.items() if 'name' in v})

    for file_name, ini in base_inis.items():
        output_file = os.path.join(OUTPUT_PATH, '%s.json' % file_name)

        if 'research' in file_name:
            convert_research(ini, output_file, ids)
        elif file_name == 'bodypropulsionimd':
            continue
        elif file_name == 'body':
            continue
        else:
            generic_convertor(ini, output_file, ids)
