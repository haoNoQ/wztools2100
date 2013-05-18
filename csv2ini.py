#!/usr/bin/python3


# USAGE:
# 	Run it in the physfs root of your mod. It will create the .ini
# 	files while leaving the .txt files intact. This will make the mod
# 	compatible with 3.2 while not breaking compatibility with 3.1.


# KNOWN ISSUES:
# 	body.ini:
# 		please review the droidType parameter manually.
# 	propulsion:ini
# 		please add the acceleration, deceleration and
# 		skidDeceleration fields manually.
# 	weapons.ini:
# 		please review the three periodicalDamageWeapon parameters
# 		manually.


from __future__ import print_function
import os.path
import string
import sys


##########################################################################
# Routines for reading and writing different file formats.

def is_something(s):
	return len(s) > 0 and not s == "0"

def list_to_ini_string(l):
	r = ""
	for (i, s) in enumerate(l):
		if i == 0:
			r += s
		else:
			r += "," + s
	return r

def yesno_to_numeric(s):
	if s == "YES":
		return "1"
	else:
		return "0"

def write_ini_section(fd, name, dic):
	fd.write("[" + name + "]\n")
	for k in sorted(dic.keys(), key = str.lower):
		v = dic[k].strip()
		if is_something(v):
			fd.write(k + " = " + v + "\n")
	fd.write("\n")

def read_csv_lines(fd, skipfirst):
	ret = []
	for line in fd:
		if skipfirst:
			skipfirst = False
			continue
		ret.append(line)
	return ret

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

messages_strings_names_txt = {}
stats_functions_txt = {}
stats_structureweapons_txt = {}
stats_structurefunctions_txt = {}

def load_stats_functions_txt():
	print("R stats/functions.txt")
	global stats_functions_txt
	fd = open("stats/functions.txt", "rt")
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
	fd.close()

def load_messages_strings_names_txt():
	print("R messages/strings/names.txt")
	global messages_strings_names_txt
	fd = open("messages/strings/names.txt", "rt")
	strlist = remove_c_style_comments(fd)
	fd.close()
	if sys.hexversion >= 0x03000000:
		trans = str.maketrans("_()\"*", "     ")
	else:
		trans = string.maketrans("_()\"*", "     ")
	for line in strlist:
		one,two = line.split(None, 1)
		messages_strings_names_txt[one] = two.translate(trans).strip()

def load_stats_structurefunctions_txt():
	print("R stats/structurefunctions.txt")
	global stats_structurefunctions_txt
	global stats_functions_txt
	fd = open("stats/structurefunctions.txt")
	for line in fd:
		l = line.split(",")
		if l[1] in stats_functions_txt:
			g = stats_functions_txt[l[1]]
			if not l[0] in stats_structurefunctions_txt:
				stats_structurefunctions_txt[l[0]] = []
			stats_structurefunctions_txt[l[0]].append(g)
	fd.close()

def load_stats_structureweapons_txt():
	print("R stats/structureweapons.txt")
	global stats_structureweapons_txt
	fd = open("stats/structureweapons.txt", "rt")
	for line in fd:
		l = line.split(",")
		r = []
		n = l[0]
		if not l[1] == "NULL":
			r.append(l[1])
		else:
			continue
		if not l[2] == "NULL":
			r.append(l[2])
		if not l[3] == "NULL":
			r.append(l[3])
		if not l[4] == "NULL":
			r.append(l[4])
		stats_structureweapons_txt[n] = r
	fd.close()

##########################################################################
# Routines to write out specific ini files.

def write_stats_body_ini():
	if not os.path.isfile("stats/body.txt"):
		return
	print("W stats/body.ini")
	fd = open("stats/body.txt", "rt")
	f = open("stats/body.ini", "wt")
	for line in read_csv_lines(fd, True):
		l = line.split(",")
		d = {}
		n = l[0]
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
		d["flameModel"] = l[23]
		d["designable"] = l[24]
		if "Person" in n:
			d["droidType"] = "BODY"
		if "Cyb" in n:
			if "Hvy" in n:
				d["droidType"] = "CYBORG_SUPER"
			else:
				d["droidType"] = "CYBORG"
		if "Mechanic" in d["name"]:
			d["droidType"] = "CYBORG_REPAIR"
		if "Engineer" in d["name"]:
			d["droidType"] = "CYBORG_CONSTRUCT"
		if "Transport" in d["name"]:
			d["droidType"] = "TRANSPORTER"
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_bodypropulsionimd_ini():
	if not os.path.isfile("stats/bodypropulsionimd.txt"):
		return
	print("W stats/bodypropulsionimd.ini")
	fd = open("stats/bodypropulsionimd.txt", "rt")
	f = open("stats/bodypropulsionimd.ini", "wt")
	dd = {}
	for line in read_csv_lines(fd, True):
		l = line.split(",")
		n = l[0]
		if not n in dd:
			dd[n] = {}
		p = l[1]
		dd[n][p] = l[2] + ", " + l[3]
	for (k, v) in dd.items():
		write_ini_section(f, k, v)
	fd.close()
	f.close()

def write_stats_construction_ini():
	if not os.path.isfile("stats/construction.txt"):
		return
	print("W stats/construction.ini")
	fd = open("stats/construction.txt", "rt")
	f = open("stats/construction.ini", "wt")
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
		d["bodyPoints"] = l[7]
		d["sensorModel"] = l[8]
		d["mountModel"] = l[9]
		d["constructPoints"] = l[10]
		d["designable"] = l[11]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_ecm_ini():
	if not os.path.isfile("stats/ecm.txt"):
		return
	print("W stats/ecm.ini")
	fd = open("stats/ecm.txt", "rt")
	f = open("stats/ecm.ini", "wt")
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
		d["body"] = l[7]
		d["sensorModel"] = l[8]
		d["mountModel"] = l[9]
		d["location"] = l[10]
		#unused = l[11]
		d["range"] = l[12]
		d["designable"] = l[13]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_features_ini():
	if not os.path.isfile("stats/features.txt"):
		return
	print("W stats/features.ini")
	fd = open("stats/features.txt", "rt")
	f = open("stats/features.ini", "wt")
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
		d["tiledraw"] = l[8]
		d["lineOfSight"] = l[9]
		d["startVisible"] = l[10]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_propulsion_ini():
	if not os.path.isfile("stats/propulsion.txt"):
		return
	print("W stats/propulsion.ini")
	fd = open("stats/propulsion.txt", "rt")
	f = open("stats/propulsion.ini", "wt")
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
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_propulsionsounds_ini():
	if not os.path.isfile("stats/propulsionsounds.txt"):
		return
	print("W stats/propulsionsounds.ini")
	fd = open("stats/propulsionsounds.txt", "rt")
	f = open("stats/propulsionsounds.ini", "wt")
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
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_propulsiontype_ini():
	if not os.path.isfile("stats/propulsiontype.txt"):
		return
	print("W stats/propulsiontype.ini")
	fd = open("stats/propulsiontype.txt", "rt")
	f = open("stats/propulsiontype.ini", "wt")
	for line in read_csv_lines(fd, False):
		l = line.split(",")
		d = {}
		n = l[0]
		d["flightName"] = l[1]
		d["multiplier"] = l[2]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_repair_ini():
	if not os.path.isfile("stats/repair.txt"):
		return
	print("W stats/repair.ini")
	fd = open("stats/repair.txt", "rt")
	f = open("stats/repair.ini", "wt")
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
		d["repairArmour"] = l[7]
		d["location"] = l[8]
		d["model"] = l[9]
		d["mountModel"] = l[10]
		d["repairPoints"] = l[11]
		d["time"] = l[12]
		d["designable"] = l[13]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_sensor_ini():
	if not os.path.isfile("stats/sensor.txt"):
		return
	print("W stats/sensor.ini")
	fd = open("stats/sensor.txt", "rt")
	f = open("stats/sensor.ini", "wt")
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
		d["bodyPoints"] = l[7]
		d["sensorModel"] = l[8]
		d["mountModel"] = l[9]
		d["range"] = l[10]
		d["location"] = l[11]
		d["type"] = l[12]
		d["time"] = l[13]
		d["power"] = l[14]
		d["designable"] = l[15]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_structure_ini():
	if not os.path.isfile("stats/structures.txt"):
		return
	print("W stats/structure.ini")
	fd = open("stats/structures.txt", "rt")
	f = open("stats/structure.ini", "wt")
	for line in read_csv_lines(fd, True):
		l = line.split(",")
		d = {}
		n = l[0]
		d["name"] = messages_strings_names_txt[n]
		d["type"] = l[1]
		#unused = l[2]
		d["strength"] = l[3]
		#unused = l[4]
		d["baseWidth"] = l[5]
		d["baseBreadth"] = l[6]
		#unused = l[7]
		d["buildPoints"] = l[8]
		d["height"] = l[9]
		d["armour"] = l[10]
		d["bodyPoints"] = l[11]
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
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_structuremodifier_ini():
	if not os.path.isfile("stats/structuremodifier.txt"):
		return
	print("W stats/structuremodifier.ini")
	fd = open("stats/structuremodifier.txt", "rt")
	f = open("stats/structuremodifier.ini", "wt")
	dd = {}
	for line in read_csv_lines(fd, True):
		l = line.split(",")
		n = l[0]
		if not n in dd:
			dd[n] = {}
		p = l[1]
		dd[n][p] = l[2]
	for (k, v) in dd.items():
		write_ini_section(f, k, v)
	fd.close()
	f.close()

def write_stats_weaponmodifier_ini():
	if not os.path.isfile("stats/weaponmodifier.txt"):
		return
	print("W stats/weaponmodifier.ini")
	fd = open("stats/weaponmodifier.txt", "rt")
	f = open("stats/weaponmodifier.ini", "wt")
	dd = {}
	for line in read_csv_lines(fd, True):
		l = line.split(",")
		n = l[0]
		if not n in dd:
			dd[n] = {}
		p = l[1]
		dd[n][p] = l[2]
	for (k, v) in dd.items():
		write_ini_section(f, k, v)
	fd.close()
	f.close()

def write_stats_weapons_ini():
	if not os.path.isfile("stats/weapons.txt"):
		return
	print("W stats/weapons.ini")
	fd = open("stats/weapons.txt", "rt")
	f = open("stats/weapons.ini", "wt")
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
		d["body"] = l[7]
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
		d["radiusHit"] = l[26]
		d["radiusDamage"] = l[27]
		d["periodicalDamageTime"] = l[28]
		d["periodicalDamage"] = l[29]
		d["periodicalDamageRadius"] = l[30]
		#unused = l[31]
		d["radiusLife"] = l[32]
		d["flightSpeed"] = l[33]
		#unused = l[34]
		d["fireOnMove"] = yesno_to_numeric(l[35])
		d["weaponClass"] = l[36]
		d["weaponSubClass"] = "\"" + l[37] + "\""
		d["movement"] = l[38]
		d["weaponEffect"] = "\"" + l[39] + "\""
		d["rotate"] = l[40]
		d["maxElevation"] = l[41]
		d["minElevation"] = l[42]
		d["facePlayer"] = yesno_to_numeric(l[43])
		d["faceInFlight"] = yesno_to_numeric(l[44])
		d["recoilValue"] = l[45]
		d["minRange"] = l[46]
		d["LightWorld"] = yesno_to_numeric(l[47])
		d["effectSize"] = l[48]
		if int(l[49]) == 1:
			flags.append("AirOnly")
		elif int(l[49]) == 100:
			flags.append("ShootAir")
		d["numAttackRuns"] = l[50]
		d["designable"] = l[51]
		d["penetrate"] = l[52]
		if is_something(d["periodicalDamage"]):
			d["periodicalDamageWeaponClass"] = d["weaponClass"]
			d["periodicalDamageWeaponSubClass"] = d["weaponSubClass"]
			d["periodicalDamageWeaponEffect"] = d["weaponEffect"]
		d["flags"] = list_to_ini_string(flags);
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_weaponsounds_ini():
	if not os.path.isfile("stats/weaponsounds.txt"):
		return
	print("W stats/weaponsounds.ini")
	fd = open("stats/weaponsounds.txt", "rt")
	f = open("stats/weaponsounds.ini", "wt")
	for line in read_csv_lines(fd, False):
		l = line.split(",")
		d = {}
		n = l[0]
		d["szWeaponWav"] = l[1]
		d["szExplosionWav"] = l[2]
		#unused = l[3]
		write_ini_section(f, n, d)
	fd.close()
	f.close()


##########################################################################
# Here goes nothing.

load_stats_functions_txt()
load_messages_strings_names_txt()
load_stats_structurefunctions_txt()
load_stats_structureweapons_txt()

write_stats_body_ini()
write_stats_bodypropulsionimd_ini()
write_stats_construction_ini()
write_stats_ecm_ini()
write_stats_features_ini()
write_stats_propulsion_ini()
write_stats_propulsiontype_ini()
write_stats_propulsionsounds_ini()
write_stats_repair_ini()
write_stats_sensor_ini()
write_stats_structure_ini()
write_stats_structuremodifier_ini()
write_stats_weaponmodifier_ini()
write_stats_weapons_ini()
write_stats_weaponsounds_ini()
