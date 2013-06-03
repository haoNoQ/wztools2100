"""
collect information about fields and values in ini file

usage run script with file name in directory with unpacked stats.

Script will collect data from all files with name.

You can specify path as second argument.

python get_ini_fields.py body.ini

python get_ini_fields.py body.ini "C:/games/warzone2100"
"""

import os
import sys
from config_parser import WZConfigParser


def get_ini_fields(fields, path):
    cp = WZConfigParser()
    cp.load(path)
    for section in cp.sections():
        for key, value in  cp.items(section):
            fields.setdefault(key, set()).add(value)


if __name__ == "__main__":
    name = sys.argv[1]
    path = sys.argv[2]
    fields = {}

    for base, dirs, files in os.walk(path):
        if name in files:
            file_path = os.path.join(base, name)
            get_ini_fields(fields, file_path)
            print "collectiong data from", file_path

    for field, values in fields.items():
        print field, ' '.join(sorted(values))

