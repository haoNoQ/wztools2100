#!/usr/bin/python3

"""
Outputs an INI diff for ini files.
  Checks:
     - difference in header
     - diffrenece in IDs
     - diffrenece in key names for each section
     - diffrenece in values for each section


usage: ini_diff.py [-h] fromfile tofile

positional arguments:
  fromfile    fromfile
  tofile      tofile

optional arguments:
  -h, --help  show this help message and exit
"""

import os
import argparse
from difflib import unified_diff
from ini_tools import WZConfigParser


def diff(file1: str, file2: str) -> None:
    for path in (file1, file2):
        if not os.path.exists(path):
            print('Error: %s does not exists' % path)
            exit(1)
    config1 = WZConfigParser()
    config1.load(file1)
    config2 = WZConfigParser()
    config2.load(file2)

    # helper function to get diff
    def diff_list(list1: list, list2: list, list_header: str) -> list:
        return list(unified_diff(list1, list2, file1, file2, n=2)), list_header

    sections1 = config1.sections()
    sections2 = config2.sections()

    diffs = [diff_list(config1.header, config2.header, "Headers diff"),
             diff_list(sections1, sections2, "Sections diff:")]

    both_sections = set(sections1).intersection(sections2)
    for section in both_sections:
        items1 = dict(config1.items(section))
        items2 = dict(config2.items(section))
        keys1 = list(items1.keys())
        keys2 =  list(items2.keys())
        keys_diff = diff_list(keys1, keys2, 'Keys diff for [%s]' % section)
        diffs.append(keys_diff)
        both_keys = set(keys1).intersection(keys2)
        values1 = []
        values2 = []
        for key in both_keys:
            values1.append('%s = %s' % (key, items1[key]))
            values2.append('%s = %s' % (key, items2[key]))
        values_diff = diff_list(values1, values2, 'Values diff for [%s]' % section)
        diffs.append(values_diff)

    diffs = [x for x in diffs if x[0]]
    if diffs:
        diffs_header = '--- tmp/%s\n+++ tmp/%s\n' % (file1, file2)
        print(diffs_header)
        for diff_result, header in diffs:
            print('%s:\n%s' % (header, ''.join([x.replace('\n', '') + '\n' for x in diff_result[3:]])))
    else:
        print("Files are same")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fromfile', help="from file")
    parser.add_argument('tofile', help="to file")
    args = parser.parse_args()
    diff(args.fromfile, args.tofile)