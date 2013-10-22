"""
collect information about fields and values in ini file

usage run script with file name in directory with unpacked stats.

Script will collect data from all files with name.

You can specify path as second argument.

python get_ini_fields.py body.ini

python get_ini_fields.py body.ini "C:/games/warzone2100"
"""
from __future__ import print_function

import os
from config_parser import WZConfigParser
import argparse


def get_ini_fields(fields, path):
    cp = WZConfigParser()
    cp.load(path)
    for section in cp.sections():
        for key, value in cp.items(section):
            fields.setdefault(key, []).append(value)


def values_to_string(values):
    values = list(set(values))
    if values:
        if values[0].isdigit():
            values.sort(key=lambda x: int(x))
        else:
            values = ['"%s"' % val.strip('''"'"''') for val in values]

    return ", ".join(values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usage: %prog [options] filename")
    parser.add_argument('name', metavar='<name>', help='name of ini file')
    parser.add_argument('path', metavar='<path>', help='path to unpacked folders. Find files in all sub folders')
    args = parser.parse_args()

    name = args.name
    path = args.path
    fields = {}

    for base, dirs, files in os.walk(path):
        if name in files:
            file_path = os.path.join(base, name)
            get_ini_fields(fields, file_path)
            print("collecting data from", file_path)

    max_size = max(map(len,  fields.values()))

    items = fields.items()
    items.sort(key=lambda x: x[0])
    for field, values in items:
        print(field, "requires=%s" % (len(values) == max_size), "values:", values_to_string(values))

