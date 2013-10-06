#!/usr/bin/python2

import sys
from ini_tools import *

data_path = None

body = None
weapons = None
propulsion = None


if __name__ == '__main__':
    config = WZConfigParser()
    config.read('tank-clasher.ini')
    if config.has_option('meta', 'data_path'):
        data_path = config.get('meta', 'data_path')
    else:
        print("Please set `data_path' in `meta' section of tank-clasher.ini")
        sys.exit()

