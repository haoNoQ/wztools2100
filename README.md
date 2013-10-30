This repository contains various simple command-line tools for working with stuff related to Warzone 2100.

_________________________

* count-oils.py:

Prints the total number oil resources on the map, including pre-placed derricks and open oil resources.

Usage: 

    python2 count-oils.py 2c-SomeMap.wz

_________________________

* ini-diff:

Finds all INI fields that are present only, or have a different value, in the second INI file compared to the first INI file, and writes them to the third file in INI format. Useful for producing diff mods supported by Warzone 2100 v3.2. Note: empty output doesn't mean first and second files are equal; second file may have some fields missing compared to the first file, and this is not detected, purposefully.

Compiling:

    qmake -project
    qmake
    make

Usage:

    ini-diff first.ini second.ini output.ini

_________________________

* validate_stats.py

prints to console errors and warnings about stats

Usage:

 python validate_stats.py [-h] [--no-warnings]

_________________________

* csv2ini.py:

An UNFINISHED converter of large stat mods from old-style comma-separated-values tables used in Warzone 2100 v3.1 or earlier into the ini format suitable for Warzone 2100 v3.2. 

Usage: 

    python3 csv2ini.py

in the directory where you have an unpacked mod. It will create ini files, making the mod compatible with the new version of the game. Some ini files will most likely need manual intervention; see comments inside the script for details.
