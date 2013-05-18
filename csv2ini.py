#!/usr/bin/python3


# USAGE:
# 	Run it in the physfs root of your mod. It will create the .ini
# 	files while leaving the .txt files intact. This will make the mod
# 	compatible with 3.2 while not breaking compatibility with 3.1.


# KNOWN ISSUES:
# 	weapons.ini:
# 		please review the three periodicalDamageWeapon parameters manually.
# 	body.ini:
# 		please review the droidType parameter manually.


import os.path


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

def write_ini_section(fd, name, dic):
	fd.write("[" + name + "]\n")
	for k in sorted(dic.keys(), key = str.lower):
		v = dic[k].strip()
		if is_something(v):
			fd.write(k + " = " + v + "\n")
	fd.write("\n")

def read_csv_lines(fd):
	ret = []
	skipfirst = True
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
					# this won't affect the next line,
					# so we're not setting comment_state
					break
				# only now we can actually do our job
				line = line.strip()
				if len(line) > 0:
					ret.append(line)
				break
	return ret


##########################################################################
# Stuff to pre-load: files referenced from many other files.

messages_strings_names_txt = {}

def load_messages_strings_names_txt():
	print("R messages/strings/names.txt")
	global messages_strings_names_txt
	fd = open("messages/strings/names.txt", "rt")
	strlist = remove_c_style_comments(fd)
	fd.close()
	trans = str.maketrans("_()\"*", "     ")
	for line in strlist:
		one,two = line.split(None, 1)
		messages_strings_names_txt[one] = two.translate(trans).strip()


##########################################################################
# Routines to write out specific ini files.

def write_stats_body_ini():
	if not os.path.isfile("stats/body.txt"):
		return
	print("W stats/body.ini")
	fd = open("stats/body.txt", "rt")
	f = open("stats/body.ini", "wt")
	for line in read_csv_lines(fd):
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
	for line in read_csv_lines(fd):
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
	for line in read_csv_lines(fd):
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
		d["sendorModel"] = l[8]
		d["mountModel"] = l[9]
		d["constructPoints"] = l[10]
		d["designable"] = l[11]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_features_ini():
	if not os.path.isfile("stats/features.txt"):
		return
	print("W stats/features.ini")
	fd = open("stats/features.txt", "rt")
	f = open("stats/features.ini", "wt")
	for line in read_csv_lines(fd):
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
		d["los"] = l[9]
		d["visible"] = l[10]
		write_ini_section(f, n, d)
	fd.close()
	f.close()

def write_stats_weapons_ini():
	if not os.path.isfile("stats/weapons.txt"):
		return
	print("W stats/weapons.ini")
	fd = open("stats/weapons.txt", "rt")
	f = open("stats/weapons.ini", "wt")
	for line in read_csv_lines(fd):
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
		d["fireOnMove"] = l[35]
		d["weaponClass"] = l[36]
		d["weaponSubClass"] = "\"" + l[37] + "\""
		d["movement"] = l[38]
		d["weaponEffect"] = "\"" + l[39] + "\""
		d["rotate"] = l[40]
		d["maxElevation"] = l[41]
		d["minElevation"] = l[42]
		d["facePlayer"] = l[43]
		d["faceInFlight"] = l[44]
		d["recoilValue"] = l[45]
		d["minRange"] = l[46]
		d["LightWorld"] = l[47]
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


##########################################################################
# Here goes nothing.

load_messages_strings_names_txt()
write_stats_body_ini()
write_stats_bodypropulsionimd_ini()
write_stats_construction_ini()
write_stats_features_ini()
write_stats_weapons_ini()

