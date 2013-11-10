#!/usr/bin/python3

# 	Run this script will make the mod
# 	compatible with 3.2 while not breaking compatibility with 3.1.

#usage: csv2ini.py [-h] [--save-path SAVE_PATH] [--rewrite] mod_path
#
#positional arguments:
#  mod_path              root folder of mod
#
#optional arguments:
#  -h, --help            show this help message and exit
#  --save-path SAVE_PATH
#                        folder to save result, if not specified save it to
#                        mod_path
#  --rewrite             If specified rewrite ini files

# KNOWN ISSUES:
# 	body.ini:
# 	*	please review the droidType parameter manually.
# 	*	please review the class parameter manually.
# 	propulsion:ini
# 	*	please add the acceleration, deceleration and
# 		skidDeceleration fields manually.
# 	weapons.ini:
# 	*	please add parameters periodicalDamage, periodicalDamageWeaponClass, periodicalDamageWeaponEffect manually if you need them.
# 	research.ini:
# 	*	we no longer support separate upgrades for factories,
# 		cyborg and VTOL factories; upgrade functions for cyborg
# 		and vtol factories are ignored by this script.
# 	*	replacedComponents are unavailable on CSV side.
#   brain.ini
#   * missed
#

from __future__ import print_function
import os.path
import string
import sys
import argparse
from ini_tools import IniFile

##########################################################################
# Globals for storing stats that will not be used instantly.

messages_strings_names_txt = {}
stats_assignweapons_txt = {}
stats_functions_txt = {}
stats_research_multiplayer_prresearch_txt = {}
stats_research_multiplayer_redcomponents_txt = {}
stats_research_multiplayer_redstructure_txt = {}
stats_research_multiplayer_researchfunctions_txt = {}
stats_research_multiplayer_resultcomponent_txt = {}
stats_research_multiplayer_resultstructure_txt = {}
stats_structureweapons_txt = {}
stats_structurefunctions_txt = {}
stats_weaponsounds_txt = {}


##########################################################################
# Routines for reading and writing different file formats.

default_overrides = {
    "fireOnMove": "1",
}


def is_something(s, k=""):
    if k in default_overrides:
        return s.strip() != default_overrides[k]
    return len(s) > 0 and not s == "0"


def list_to_ini_string(l):
    return ",".join(l)


def yesno_to_numeric(s):
    return s == "YES" and "1" or "0"


def read_csv_lines(fd, skip_first):
    # TODO strip each line before adding to list, and check if something present
    # ret = [line.strip() for line in fd if line(strip)]
    return (x.strip() for x in list(fd)[skip_first:])


# returns a list of strings which represent non-empty lines of file fd
# with all C-style comments eliminated
def remove_c_style_comments(fd):
    ret = []
    comment_state = False
    for line in fd:
        while True:
            # seems we have nothing left
            if len(line) < 2:
                break
            # we're still inside a comment
            if comment_state:
                idx = line.find("*/")
                if idx > -1:
                    line = line[idx + 2:]
                    comment_state = False
                    continue
                # comment doesn't seem to end on this line
                break
            # we're not inside any comment
            else:
                idx = line.find("/*")
                if idx > -1:
                    line = line[idx + 2:]
                    comment_state = True
                    continue
                if "//" in line:
                    line = line.split("//", 1)[0]
                # only now we can actually do our job
                line = line.strip()
                if len(line) > 0:
                    ret.append(line)
                break
    return ret


##########################################################################
# Stuff to pre-load: files referenced from many other files.

def load_messages_strings_names_txt(path):
    path = os.path.join(path, "messages", "strings", "names.txt")
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        str_list = remove_c_style_comments(fd)

    if sys.hexversion >= 0x03000000:
        trans = str.maketrans("_()\"", "    ")
    else:
        trans = string.maketrans("_()\"", "    ")
    for line in str_list:
        one, two = line.split(None, 1)
        messages_strings_names_txt[one] = two.translate(trans).strip()


def load_stats_assignweapons_txt(path):
    path = os.path.join(path, "stats", "assignweapons.txt")
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in fd:
            l = line.split(",")
            r = []
            n = l[0]
            if not l[1] == "NULL" and is_something(l[1]):
                r.append(l[1])
            else:
                continue
            if not l[2] == "NULL" and is_something(l[2]):
                r.append(l[2])
            if not l[3] == "NULL" and is_something(l[3]):
                r.append(l[3])
            stats_assignweapons_txt[n] = r


def load_stats_functions_txt(path):
    path = os.path.join(path, "stats", "functions.txt")
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        stats_upgrades = {}
        def throw_in_upgrade(key, func, val):
            if not key in stats_upgrades:
                stats_upgrades[key] = []
            stats_upgrades[key].append((func, int(val)))
        for line in fd:
            l = line.split(",")
            g = l[0]
            n = l[1]
            if g == "Production":
                stats_functions_txt[n] = ("productionPoints", l[3])
            elif g == "Power Generator":
                stats_functions_txt[n] = ("powerPoints", l[3])
            elif g == "Research":
                stats_functions_txt[n] = ("researchPoints", l[2])
            elif g == "Repair Droid":
                stats_functions_txt[n] = ("repairPoints", l[2])
            elif g == "ReArm":
                stats_functions_txt[n] = ("rearmPoints", l[2])
            elif g == "Research Upgrade":
                throw_in_upgrade("ResearchPoints", n, l[2])
            elif g == "Production Upgrade":
                if l[2].strip() == "1":
                    throw_in_upgrade("ProductionPoints", n, l[5])
            elif g == "Weapon Upgrade":
                t = l[2]
                if int(l[3]) > 0:
                    throw_in_upgrade(t + ":FirePause", n, l[3])
                if int(l[4]) > 0:
                    throw_in_upgrade(t + ":HitChance", n, l[4])
                if int(l[6]) > 0:
                    throw_in_upgrade(t + ":Damage", n, l[6])
                if int(l[7]) > 0:
                    throw_in_upgrade(t + ":RadiusDamage", n, l[7])
                if int(l[8]) > 0:
                    throw_in_upgrade(t + ":RepeatDamage", n, l[8])
            elif g == "Structure Upgrade":
                if int(l[3]) > 0:
                    throw_in_upgrade("Structure:HitPoints", n, l[3])
                if int(l[2]) > 0:
                    throw_in_upgrade("Structure:Armour", n, l[2])
                if int(l[4]) > 0:
                    throw_in_upgrade("Structure:Resistance", n, l[4])
                    throw_in_upgrade("Droids:Resistance", n, l[4])
            elif g == "WallDefence Upgrade":
                if int(l[2]) > 0:
                    throw_in_upgrade("Wall:Armour", n, l[2])
                if int(l[3]) > 0:
                    throw_in_upgrade("Wall:HitPoints", n, l[3])
            elif g == "Repair Upgrade":
                throw_in_upgrade("RepairPoints", n, l[2])
            elif g == "Power Upgrade":
                throw_in_upgrade("PowerPoints", n, l[2])
            elif g == "VehicleBody Upgrade":
                applies = []
                if l[6].strip() == "1":
                    applies.append("Droids")
                if l[7].strip() == "1":
                    applies.append("Cyborgs")
                for t in applies:
                    if int(l[2]) > 0:
                        throw_in_upgrade(t + ":Power", n, l[2])
                    if int(l[4]) > 0:
                        throw_in_upgrade(t + ":Armour", n, l[4])
                    if int(l[3]) > 0:
                        throw_in_upgrade(t + ":HitPoints", n, l[3])
                    if int(l[5]) > 0:
                        throw_in_upgrade(t + ":Thermal", n, l[5])
            elif g == "VehicleConst Upgrade":
                throw_in_upgrade("Construct:ConstructorPoints", n, l[2])
            elif g == "VehicleECM Upgrade":
                throw_in_upgrade("ECM:Range", n, l[2])
            elif g == "VehicleSensor Upgrade":
                throw_in_upgrade("Sensor:Range", n, l[3])
            elif g == "ReArm Upgrade":
                throw_in_upgrade("RearmPoints", n, l[2])

    def throw_in_function(key, func, value):
        if not func in stats_functions_txt:
            stats_functions_txt[func] = []
        if "FirePause" in key:
            stats_functions_txt[func].append((key, str(-value)))
        else:
            stats_functions_txt[func].append((key, str(value)))

    for k in stats_upgrades.keys():
        if len(stats_upgrades[k]) == 0:
            continue
        lst = sorted(stats_upgrades[k], key=lambda x: x[1])
        throw_in_function(k, lst[0][0], lst[0][1])
        i = 1
        while i < len(lst):
            throw_in_function(k, lst[i][0], lst[i][1] - lst[i - 1][1])
            i += 1

    fd.close()


def load_stats_research_multiplayer_prresearch_txt(path):
    path = os.path.join(path, 'stats', 'research', 'multiplayer','prresearch.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_prresearch_txt:
                stats_research_multiplayer_prresearch_txt[l[0]] = []
            stats_research_multiplayer_prresearch_txt[l[0]].append(l[1])


def load_stats_research_multiplayer_redcomponents_txt(path):
    path = os.path.join(path, 'stats', 'research', 'multiplayer', 'redcomponents.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_redcomponents_txt:
                stats_research_multiplayer_redcomponents_txt[l[0]] = []
            stats_research_multiplayer_redcomponents_txt[l[0]].append(l[1])


def load_stats_research_multiplayer_redstructure_txt(path):
    path = os.path.join(path, 'stats', 'research', 'multiplayer', 'redstructure.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_redstructure_txt:
                stats_research_multiplayer_redstructure_txt[l[0]] = []
            stats_research_multiplayer_redstructure_txt[l[0]].append(l[1])


def load_stats_research_multiplayer_researchfunctions_txt(path):
    path = os.path.join(path, 'stats', 'research', 'multiplayer', 'researchfunctions.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_researchfunctions_txt:
                stats_research_multiplayer_researchfunctions_txt[l[0]] = []
            stats_research_multiplayer_researchfunctions_txt[l[0]].append(l[1])


def load_stats_research_multiplayer_resultcomponent_txt(path):
    path = os.path.join(path, 'stats', 'research' ,'multiplayer' ,'resultcomponent.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_resultcomponent_txt:
                stats_research_multiplayer_resultcomponent_txt[l[0]] = []
            stats_research_multiplayer_resultcomponent_txt[l[0]].append(l[1])



def load_stats_research_multiplayer_resultstructure_txt(path):
    path = os.path.join(path, 'stats', 'research', 'multiplayer', 'resultstructure.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            if not l[0] in stats_research_multiplayer_resultstructure_txt:
                stats_research_multiplayer_resultstructure_txt[l[0]] = []
            stats_research_multiplayer_resultstructure_txt[l[0]].append(l[1])


def load_stats_structurefunctions_txt(path):
    path = os.path.join(path, 'stats', 'structurefunctions.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in fd:
            l = line.split(",")
            if l[1] in stats_functions_txt:
                g = stats_functions_txt[l[1]]
                if not l[0] in stats_structurefunctions_txt:
                    stats_structurefunctions_txt[l[0]] = []
                stats_structurefunctions_txt[l[0]].append(g)


def load_stats_structureweapons_txt(path):
    path = os.path.join(path, 'stats', 'structureweapons.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in fd:
            l = line.split(",")
            r = []
            n = l[0]
            if not l[1] == "NULL" and is_something(l[1]):
                r.append(l[1])
            else:
                continue
            if not l[2] == "NULL" and is_something(l[2]):
                r.append(l[2])
            if not l[3] == "NULL" and is_something(l[3]):
                r.append(l[3])
            if not l[4] == "NULL" and is_something(l[4]):
                r.append(l[4])
            stats_structureweapons_txt[n] = r


def load_stats_weaponsounds_txt(path):
    path = os.path.join(path, 'stats', 'weaponsounds.txt')
    if not os.path.isfile(path):
        return
    with open(path) as fd:
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            n = l[0]
            stats_weaponsounds_txt[n] = (l[1], l[2])


##########################################################################
# Routines to write out specific ini files.


class BaseConverter(object):
    SOURCE = None
    DEST = None  # optional

    def __init__(self, mod_path, save_path, rewrite):
        assert self.SOURCE, "SOURCE must be defined"
        self.dest = self.DEST or self.SOURCE.replace(".txt", '.ini')



        source_file = os.path.join(mod_path, self.SOURCE)
        self.dest_file = os.path.join(save_path, self.dest)


        if not rewrite and os.path.exists(self.dest_file):
            print("Skipping %s, file %s already exists" % (self.SOURCE, self.dest_file))
            return
        with open(source_file, 'r') as fd:
            data = self.convert(fd)
            assert data is not None
        self.write(data)
        print("Writing %s" % self.dest_file)

    def convert(self, fd):
        raise NotImplemented("Implement in children")

    def write(self, data_dict):
        ini_file = IniFile(self.dest_file, data_dict)
        ini_file.save(self.dest_file)


class ConvertBodypropulsionimd(BaseConverter):
    SOURCE = 'stats/bodypropulsionimd.txt'

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            key, item_key, v1, v2 = line.split(",")[:4]
            dd.setdefault(key, {})[item_key] = '%s,%s' % (v1, v2)
        return dd


class ConvertBody(BaseConverter):
    SOURCE = "stats/body.txt"

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            n = l[0]
            d = {}
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["size"] = l[2]
            d["buildPower"] = l[3]
            d["buildPoints"] = l[4]
            d["weight"] = l[5]
            d["hitpoints"] = l[6]
            d["model"] = l[7]
            #unused = l[8]
            d["weaponSlots"] = l[9]
            d["powerOutput"] = l[10]
            d["armourKinetic"] = l[11]
            d["armourHeat"] = l[12]
            #unused = l[13]
            #unused = l[14]
            #unused = l[15]
            #unused = l[16]
            #unused = l[17]
            #unused = l[18]
            #unused = l[19]
            #unused = l[20]
            #unused = l[21]
            #unused = l[22]
            d["designable"] = l[24]
            d["class"] = "Droids"
            if "Person" in n:
                d["droidType"] = "PERSON"
                d["class"] = "Babas"
            if "Cyb" in n:
                if "Hvy" in n:
                    d["droidType"] = "CYBORG_SUPER"
                else:
                    d["droidType"] = "CYBORG"
                d["class"] = "Cyborgs"
            if "Mechanic" in d["name"]:
                d["droidType"] = "CYBORG_REPAIR"
                d["class"] = "Cyborgs"
            if "Engineer" in d["name"]:
                d["droidType"] = "CYBORG_CONSTRUCT"
                d["class"] = "Cyborgs"
            if "Transport" in d["name"]:
                d["droidType"] = "TRANSPORTER"
                d["class"] = "Transports"
            dd[n] = d
        return dd


class ConvertConstructions(BaseConverter):
    SOURCE = "stats/construction.txt"

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["hitpoints"] = l[7]
            d["sensorModel"] = l[8]
            d["mountModel"] = l[9]
            d["constructPoints"] = l[10]
            d["designable"] = l[11]
            dd[n] = d
        return dd


class ConvertBrain(BaseConverter):
    SOURCE = "stats/brain.txt"
    def convert(self, fd):
        dd= {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["turret"] = l[7]

            # add some default values
            d["maxDroids"] = 6
            d["maxDroidsMult"] = 2
            if n != 'ZNULLBRAIN':
                d["designable"] = 1
            dd[n] = d
        return dd


class ConvertEcm(BaseConverter):
    SOURCE = "stats/ecm.txt"
    def convert(self, fd):
        dd= {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["hitpoints"] = l[7]
            d["sensorModel"] = l[8]
            d["mountModel"] = l[9]
            d["location"] = l[10]
            #unused = l[11]
            d["range"] = l[12]
            d["designable"] = l[13]
            dd[n] = d
        return dd

class ConvertFeatures(BaseConverter):
    SOURCE = "stats/features.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            d["width"] = l[1]
            d["breadth"] = l[2]
            d["damageable"] = l[3]
            d["armour"] = l[4]
            d["hitpoints"] = l[5]
            d["model"] = l[6]
            d["type"] = l[7]
            d["tileDraw"] = l[8]
            d["lineOfSight"] = l[9]
            d["startVisible"] = l[10]
            dd[n] = d
        return dd


class ConvertPropulsion(BaseConverter):
    SOURCE = "stats/propulsion.txt"

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["hitpoints"] = l[7]
            d["model"] = l[8]
            d["type"] = l[9]
            d["speed"] = l[10]
            d["designable"] = l[11]
            dd[n] = d
        return dd

class ConvertPropulsionSounds(BaseConverter):
    SOURCE = "stats/propulsionsounds.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["szStart"] = l[1]
            d["szIdle"] = l[2]
            d["szMoveOff"] = l[3]
            d["szMove"] = l[4]
            d["szHiss"] = l[5]
            d["szShutDown"] = l[6]
            #unused = l[7]
            dd[n] = d
        return dd

class ConvertPropulsionType(BaseConverter):
    SOURCE = "stats/propulsiontype.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["flightName"] = l[1]
            d["multiplier"] = l[2]
            dd[n] = d
        return dd

class ConvertResearch(BaseConverter):
    SOURCE = "stats/research/multiplayer/research.txt"
    DEST = "stats/research.ini"

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["subgroupIconID"] = l[2]
            d["techCode"] = l[3]
            d["iconID"] = l[4]
            d["imdName"] = l[5]
            #unused = l[6]
            d["msgName"] = l[7]
            if not l[8] == "0":
                d["statID"] = l[8]
            if not l[9] == "0":
                d["statID"] = l[9]
            #unused = l[10]
            d["researchPoints"] = l[11]
            p = int(int(l[11]) / 32)
            if p > 450:
                p = 450
            d["researchPower"] = str(p)
            d["keyTopic"] = l[12]
            #unused = l[13]
            #unused = l[14]
            #unused = l[15]
            #unused = l[16]
            #unused = l[17]
            #unused = l[18]
            #unused = l[19]
            if n in stats_research_multiplayer_prresearch_txt:
                p = stats_research_multiplayer_prresearch_txt[n]
                d["requiredResearch"] = list_to_ini_string(p)
            if n in stats_research_multiplayer_redcomponents_txt:
                p = stats_research_multiplayer_redcomponents_txt[n]
                d["redComponents"] = list_to_ini_string(p)
            if n in stats_research_multiplayer_redstructure_txt:
                p = stats_research_multiplayer_redstructure_txt[n]
                d["redStructures"] = list_to_ini_string(p)
            if n in stats_research_multiplayer_resultcomponent_txt:
                p = stats_research_multiplayer_resultcomponent_txt[n]
                d["resultComponents"] = list_to_ini_string(p)
            if n in stats_research_multiplayer_resultstructure_txt:
                p = stats_research_multiplayer_resultstructure_txt[n]
                d["resultStructures"] = list_to_ini_string(p)
            if n in stats_research_multiplayer_researchfunctions_txt:
                lst = []
                for g in stats_research_multiplayer_researchfunctions_txt[n]:
                    if g in stats_functions_txt:
                        lst += stats_functions_txt[g]
                i = 0
                s = ""
                while i < len(lst):
                    if i > 0:
                        s += ", "
                    s += "\"" + lst[i][0] + ":" + lst[i][1] + "\""
                    i += 1
                d["results"] = s
            dd[n] = d
        return dd


class ConvertRepair(BaseConverter):
    SOURCE = "stats/repair.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            #d["repairArmour"] = l[7] not used
            d["location"] = l[8]
            d["model"] = l[9]
            d["mountModel"] = l[10]
            d["repairPoints"] = l[11]
            d["time"] = l[12]
            d["designable"] = l[13]
            dd[n] = d
        return dd


class ConvertSensor(BaseConverter):
    SOURCE = "stats/sensor.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            d = {}
            n = l[0]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["hitpoints"] = l[7]
            d["sensorModel"] = l[8]
            d["mountModel"] = l[9]
            d["range"] = l[10]
            d["location"] = l[11]
            d["type"] = l[12]
            d["time"] = l[13]
            d["power"] = l[14]
            d["designable"] = l[15]
            dd[n] = d
        return dd


class ConvertStructure(BaseConverter):
    SOURCE = "stats/structures.txt"
    DEST = "stats/structure.ini"
    
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            if l[1] == "DOOR":
                l[1] = "DEFENSE"
            d["type"] = l[1]
            #unused = l[2]
            d["strength"] = l[3]
            #unused = l[4]
            d["width"] = l[5]
            d["breadth"] = l[6]
            #unused = l[7]
            d["buildPoints"] = l[8]
            d["height"] = l[9]
            d["armour"] = l[10]
            d["hitpoints"] = l[11]
            #unused = l[12]
            d["buildPower"] = l[13]
            #unused = l[14]
            d["resistance"] = l[15]
            #unused = l[16]
            #unused = l[17]
            if not l[18] == "ZNULLECM":
                d["ecmID"] = l[18]
            if not l[19] == "ZNULLSENSOR":
                d["sensorID"] = l[19]
            #unused = l[20]
            d["structureModel"] = l[21].replace("@", ", ")
            d["baseModel"] = l[22]
            #unused = l[23]
            if n in stats_structureweapons_txt:
                d["weapons"] = list_to_ini_string(stats_structureweapons_txt[n])
            if n in stats_structurefunctions_txt:
                for g in stats_structurefunctions_txt[n]:
                    d[g[0]] = g[1]
            dd[n] = d
        return dd


class ConvertStructureModifier(BaseConverter):
    SOURCE = "stats/structuremodifier.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            n = l[0]
            if not n in dd:
                dd[n] = {}
            p = l[1]
            dd[n][p] = l[2]
        return dd

class ConvertTemplates(BaseConverter):
    SOURCE = "stats/templates.txt"

    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            d = {}
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["compBody"] = l[2]
            if l[3] != "ZNULLBRAIN":
                d["compBrain"] = l[3]
            if l[4] != "ZNULLCONSTRUCT":
                d["compConstruct"] = l[4]
            #unused = l[5]
            d["available"] = yesno_to_numeric(l[6])
            d["compPropulsion"] = l[7]
            if l[8] != "ZNULLREPAIR":
                d["compRepair"] = l[8]
            d["type"] = l[9]
            if not l[10] == "ZNULLSENSOR":
                d["compSensor"] = l[10]
            if n in stats_assignweapons_txt:
                d["weapons"] = list_to_ini_string(stats_assignweapons_txt[n])
            dd[n] = d
        return dd


class ConvertTerrainTable(BaseConverter):
    SOURCE = "stats/terraintable.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            n = l[0]
            dd.setdefault(n, []).append(l[2].strip())
        return {k: {"speedFactor": ','.join(v)} for k, v in dd.items()}


class ConvertWepornModifier(BaseConverter):
    SOURCE = "stats/weaponmodifier.txt"
    def convert(self, fd):
        dd = {}
        for line in read_csv_lines(fd, False):
            l = line.split(",")
            n = l[0]
            if not n in dd:
                dd[n] = {}
            p = l[1]
            dd[n][p] = l[2]
        return dd


class ConvertWeaporns(BaseConverter):
    SOURCE = "stats/weapons.txt"
    def convert(self, fd):
        dd= {}
        for line in read_csv_lines(fd, True):
            l = line.split(",")
            d = {}
            flags = []
            n = l[0]
            d["name"] = messages_strings_names_txt[n]
            #unused = l[1]
            d["buildPower"] = l[2]
            d["buildPoints"] = l[3]
            d["weight"] = l[4]
            #unused = l[5]
            #unused = l[6]
            d["hitpoints"] = l[7]
            d["model"] = l[8]
            d["mountModel"] = l[9]
            d["muzzleGfx"] = l[10]
            d["flightGfx"] = l[11]
            d["hitGfx"] = l[12]
            d["missGfx"] = l[13]
            d["waterGfx"] = l[14]
            #unused = l[15]
            #unused = l[16]
            d["longRange"] = l[17]
            #unused = l[18]
            d["longHit"] = l[19]
            d["firePause"] = l[20]
            d["numExplosions"] = l[21]
            d["numRounds"] = l[22]
            d["reloadTime"] = l[23]
            d["damage"] = l[24]
            d["radius"] = l[25]
            #unused = l[26]
            d["radiusDamage"] = l[27]
            d["periodicalDamageTime"] = l[28]
            d["periodicalDamage"] = l[29]
            d["periodicalDamageRadius"] = l[30]
            #unused = l[31]
            d["radiusLife"] = l[32]
            d["flightSpeed"] = l[33]
            #unused = l[34]
            d["fireOnMove"] = yesno_to_numeric(l[35])
            if l[36] == "MISC":
                l[36] = "KINETIC"
            d["weaponClass"] = l[36]
            d["weaponSubClass"] = l[37]
            if l[38] == "ERRATIC-DIRECT":
                l[38] = "DIRECT"
            d["movement"] = l[38]
            d["weaponEffect"] = l[39]
            d["rotate"] = l[40]
            d["maxElevation"] = l[41]
            d["minElevation"] = l[42]
            d["facePlayer"] = yesno_to_numeric(l[43])
            d["faceInFlight"] = yesno_to_numeric(l[44])
            d["recoilValue"] = l[45]
            d["minRange"] = l[46]
            d["lightWorld"] = yesno_to_numeric(l[47])
            d["effectSize"] = l[48]
            if l[49] == '1':
                d["flags"] = "AirOnly"
            elif l[49] == '100':
                d["flags"] = "ShootAir"
            else:
                d["flags"] = l[49]

            d["numAttackRuns"] = l[50]
            d["designable"] = l[51]
            d["penetrate"] = l[52]
            if n in stats_weaponsounds_txt:
                s = stats_weaponsounds_txt[n][0].strip()
                if s != "-1":
                    d["weaponWav"] = s
                s = stats_weaponsounds_txt[n][1].strip()
                if s != "-1":
                    d["explosionWav"] = s
            d["minimumDamage"] = "33"
            dd[n] = d
        return dd


##########################################################################
# Here goes nothing.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='mod_path', help="root folder of mod")
    parser.add_argument('--save-path', help="folder to save result, if not specified save it to mod_path")
    parser.add_argument('--rewrite', help="If specified rewrite ini files", action="store_true")
    args = parser.parse_args()

    path=args.mod_path
    save_path = args.save_path
    if save_path is None:
        save_path = path
    rewrite = args.rewrite

    load_messages_strings_names_txt(path)
    load_stats_assignweapons_txt(path)
    load_stats_functions_txt(path)
    load_stats_research_multiplayer_prresearch_txt(path)
    load_stats_research_multiplayer_redcomponents_txt(path)
    load_stats_research_multiplayer_redstructure_txt(path)
    load_stats_research_multiplayer_researchfunctions_txt(path)
    load_stats_research_multiplayer_resultcomponent_txt(path)
    load_stats_research_multiplayer_resultstructure_txt(path)
    load_stats_structurefunctions_txt(path)
    load_stats_structureweapons_txt(path)
    load_stats_weaponsounds_txt(path)

    ConvertBodypropulsionimd(path, save_path, rewrite)
    ConvertBody(path, save_path, rewrite)
    ConvertConstructions(path, save_path, rewrite)
    ConvertEcm(path, save_path, rewrite)
    ConvertFeatures(path, save_path, rewrite)
    ConvertPropulsion(path, save_path, rewrite)
    ConvertPropulsionType(path, save_path, rewrite)
    ConvertBodypropulsionimd(path, save_path, rewrite)
    ConvertResearch(path, save_path, rewrite)
    ConvertRepair(path, save_path, rewrite)
    ConvertSensor(path, save_path, rewrite)
    ConvertStructure(path, save_path, rewrite)
    ConvertStructureModifier(path, save_path, rewrite)
    ConvertTemplates(path, save_path, rewrite)
    ConvertTerrainTable(path, save_path, rewrite)
    ConvertWepornModifier(path, save_path, rewrite)
    ConvertWeaporns(path, save_path, rewrite)
    ConvertBrain(path, save_path, rewrite)





