#!/usr/bin/python3

"""
Remove entries from names.txt that already present in ini files.
This script will be need once then template names will be moved to ini files

usage:
python cleanup_names.txt.py
"""

import os
import re
import sys
sys.path.insert(0, '../ini_tools')
from enviroment import BASE_PATH, MP_PATH
from ini_file import IniFile

name_reg = re.compile('^([\w-]+)[ \t]+(.*)')

def clean(module_path, module_name):
    print("Cleaning %s(%s)" % (module_name, module_path))
    ini_names = {}
    names_path = os.path.join(module_path, 'messages', 'strings', 'names.txt')
    stats_dir =os.path.join(module_path, 'stats')
    files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
    for path in files:
        ini_file = IniFile(os.path.join(stats_dir, path))
        for k, v in ini_file.items():
            if 'name' in v:
                ini_names[k] = v['name']

    new_names = []
    with open(names_path) as f:
        for line in f:
            line = line.strip('\n\r')
            match = name_reg.match(line)
            if match:
                key = match.group(1)
                value = match.group(2)
                if key in ini_names:
                    if value.strip('"_() ') != ini_names[key].strip('"_() '):
                        print(key, value, ini_names[key])
                else:
                    new_names.append(line)
            else:
                new_names.append(line)

    with open('%s_names.txt' % module_name, 'w') as f:
        f.write('\n'.join(new_names))

if __name__ == '__main__':
    clean(BASE_PATH, 'base')
    clean(MP_PATH, 'mp')
