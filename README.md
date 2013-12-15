This repository contains various simple command-line tools for working with stuff related to Warzone 2100.

_________________________


#### [count-oils.py](../blob/master/count_oils.py)

Prints the total number oil resources on the map, including pre-placed derricks and open oil resources.

```
usage: python2 count-oils.py 2c-SomeMap.wz
```


#### [csv2ini.py](../blob/master/csv2ini.py)

Convert txt files to ini. 
Scripts works with unpacked folder, check known issues before use.

```
usage: csv2ini.py [-h] [--save-path SAVE_PATH] [--rewrite] mod_path

positional arguments:
  mod_path              root folder of mod

optional arguments:
  -h, --help            show this help message and exit
  --save-path SAVE_PATH
                        folder to save result, if not specified save it to
                        mod_path
  --rewrite             If specified rewrite ini files
```

##### known issues:

 	body.ini:
 	*	please review the droidType parameter manually.
 	*	please review the class parameter manually.
 	propulsion:ini
 	*	please add the acceleration, deceleration and skidDeceleration fields manually.
 	weapons.ini:
 	*	please add parameters periodicalDamage, periodicalDamageWeaponClass,
 	    periodicalDamageWeaponEffect manually if you need them.
 	research.ini:
 	*	we no longer support separate upgrades for factories,
 		cyborg and VTOL factories; upgrade functions for cyborg
 		and vtol factories are ignored by this script.
 	*	replacedComponents are unavailable on CSV side.

_________________________


#### [validate_stats.py](../blob/master/validate_stats.py)

Prints to console errors and warnings about stats


```
usage: validate_stats.py [-h] [--no-warnings] <modpath> <basepath>

positional arguments:
  <modpath>      path to mod folder
  <basepath>     path to base folder

optional arguments:
  -h, --help     show this help message and exit
  --no-warnings  don't show warnings
```

_________________________


#### [ini-diff](../blob/matser/ini-diff/main.cpp)

Finds all INI fields that are present only, or have a different value, in the second INI file compared to the first INI file, and writes them to the third file in INI format. Useful for producing diff mods supported by Warzone 2100 v3.2. Note: empty output doesn't mean first and second files are equal; second file may have some fields missing compared to the first file, and this is not detected, purposefully.

##### Compiling

    qmake -project
    qmake
    make

```
usage: ini-diff first.ini second.ini output.ini
```

_________________________


#### [ini_diff.py](../blob/master/ini_diff.py)

This is another ini diff. Prints diff between fromfile and tofile. Show differences in Ids, keys and vals

```
usage: ini_diff.py [-h] fromfile tofile

positional arguments:
  fromfile    from file
  tofile      to file

optional arguments:
  -h, --help  show this help message and exit
```
