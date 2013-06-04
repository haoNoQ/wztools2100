#!/usr/bin/python2

# usage:
#     count-oils.py 2c-SomeMap.wz

# Counts oil resources on the map. This includes oils under derricks and
# unoccupied oils, which sometimes may overlap, hence the complexity.
# Works with both old-style binary format maps and new-style ini format maps.

import sys
import zipfile

mapfile = sys.argv[1]
wzfile = zipfile.ZipFile(mapfile)
oillist = []

def findfile(filename):
    global wzfile
    for path in wzfile.namelist():
        if (path.endswith(filename)):
            return wzfile.open(path, "r")

def add_to_oillist(x, y):
    global oillist
    oillist.append(str(x) + " " + str(y))

def safe_close(fd):
    try:
      fd.close()
    except:
      return

def read_ini_sections(fd):
    ret = {}
    try:
        line = fd.readline()
    except:
        return ret
    nm = ""
    while line != "":
        if '[' in line:
            nm = line.strip()[1:-1]
            ret[nm] = {}
        else:
            try:
                key, value = line.split('=')
            except:
                line = fd.readline()
                continue
            ret[nm][key.strip()] = value.strip()
        line = fd.readline()
    return ret

def parse_feature_ini(fd):
    sections = read_ini_sections(fd)
    for sname, section in sections.iteritems():
        if section["name"] == "OilResource":
            x, y = section["position"].replace(',', '').split()[0:2]
            add_to_oillist(int(x) / 128, int(y) / 128)
    safe_close(fd)

def parse_struct_ini(fd):
    sections = read_ini_sections(fd)
    for sname, section in sections.iteritems():
        if section["name"] == "A0ResourceExtractor":
            x, y = section["position"].replace(',', '').split()[0:2]
            add_to_oillist(int(x) / 128, int(y) / 128)
    safe_close(fd)

def parse_feat_bjo(fd):
    try:
        fd.read(12)
    except:
        return
    while True:
        s = fd.read(76)
        if s == "":
            break
        if not s.startswith("OilResource"):
            continue
        s = s[44:50]
        x = (ord(s[1]) * 256 + ord(s[0])) / 128
        y = (ord(s[5]) * 256 + ord(s[4])) / 128
        add_to_oillist(x, y) 
    safe_close(fd)

def parse_struct_bjo(fd):
    try:
        fd.read(12)
    except:
        return
    while True:
        s = fd.read(120)
        if s == "":
            break
        if not s.startswith("A0ResourceExtractor"):
            continue
        s = s[44:50]
        x = (ord(s[1]) * 256 + ord(s[0])) / 128
        y = (ord(s[5]) * 256 + ord(s[4])) / 128
        add_to_oillist(x, y)
    safe_close(fd)

if __name__ == "__main__":
    parse_feature_ini(findfile("feature.ini"))
    parse_struct_ini(findfile("struct.ini"))
    parse_feat_bjo(findfile("feat.bjo"))
    parse_struct_bjo(findfile("struct.bjo"))
    print len(list(set(oillist)))
