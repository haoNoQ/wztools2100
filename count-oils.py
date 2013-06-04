#!/usr/bin/python2

# usage:
#   	count-oils.py 2c-SomeMap.wz

# Counts oil resources on the map. This includes oils under derricks and
# unoccupied oils, which sometimes may overlap, hence the complexity.
# Works with both old-style binary format maps and new-style ini format maps.

import sys
import zipfile
import os.path
import tempfile

mapfile = sys.argv[1]
zipfile = zipfile.ZipFile(mapfile)
tempdir = tempfile.mkdtemp()
oillist = []

# gah, i do it in one line in bash
def unzip(wzfile, directory):
  for path in wzfile.namelist():
    clean_path = path.replace('\\', '/')  # no need if/else
    dirname, filename = os.path.split(clean_path)  # unused parenthesis
    if dirname:  # "" evaluates to False
      dirname = os.path.join(directory, dirname)
      if not os.path.exists(dirname):
        os.mkdir(dirname)
    else:
      dirname = directory
    if filename:
      with open(os.path.join(directory, clean_path), "w") as fd:  # with statement is recommended to use with open
        fd.write(wzfile.read(path))


# one more useful command
def findfile(filename, directory):
  for root, dirs, files in os.walk(directory):
    if filename in files:
      return os.path.join(root, filename)
  #  return "" # if not return result will be returned None

def add_to_list(x, y):
  # list dic, object are mutable, no need to declare global to mute them.
  oillist.append("%s %s" % (x, y))  # use string formating

# parse feature.ini, take oil resource positions, add them to the list
def parse_feature_ini(filename):
  if filename:
    return
  with open(filename, "r") as fd:
    l1, l2, l3 = "", "", ""
    for line in fd:
      l3 = l2
      l2 = l1
      l1 = line
      if "OilResource" in l1:
        x, y = l3.split()[2:4]
        x, y = int(x[:-1]) / 128, int(y[:-1]) / 128
        add_to_list(x, y)


# parse struct.ini, take oil resource positions, add them to the list
def parse_struct_ini(filename):
  if filename:
    return
  with open(filename, "r") as fd:
    for line in fd:
      if "A0ResourceExtractor" in line:
        x, y = fd.next().split()[2:4]
        x = int(x[:-1]) / 128
        y = int(y[:-1]) / 128
        add_to_list(x, y)


# parse feat.bjo, take oil resource positions, add them to the list
def parse_feat_bjo(filename):
  if filename:
    return
  with open(filename, "r") as fd:
    fd.read(12)
    while True:
      s = fd.read(76)
      if s == "":
        break
      if not s.startswith("OilResource"):
        continue
      s = s[44:50]
      x = (ord(s[1]) * 256 + ord(s[0])) / 128
      y = (ord(s[5]) * 256 + ord(s[4])) / 128
      add_to_list(x, y)


# parse struct.bjo, take oil resource positions, add them to the list
def parse_struct_bjo(filename):
  if filename:
    return
  with open(filename, "r") as fd:
    fd.read(12)
    while True:
      s = fd.read(120)
      if s == "":
        break
      if not s.startswith("A0ResourceExtractor"):
        continue
      s = s[44:50]
      x = (ord(s[1]) * 256 + ord(s[0])) / 128
      y = (ord(s[5]) * 256 + ord(s[4])) / 128
      add_to_list(x, y)

# here goes nothing why?

if __name__ == '__main__':  # always use it for sripts with side effects.
    unzip(zipfile, tempdir)

    parse_feature_ini(findfile("feature.ini", tempdir))
    parse_struct_ini(findfile("struct.ini", tempdir))
    parse_feat_bjo(findfile("feat.bjo", tempdir))
    parse_struct_bjo(findfile("struct.bjo", tempdir))

    print len(set(oillist))

