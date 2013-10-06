import os
from ini_file import IniFile, WZException
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stats_folders', help='list of folders with ini files', nargs='+')
    parser.add_argument('--no-warnings', dest='no_warnings', action='store_true',
                        help="don't show warnings")


    args = parser.parse_args()

    stats_paths = args.stats_folders
    if not all([os.path.exists(path) for path in stats_paths]):
        print "Invalid paths:", [path for path in stats_paths if not os.path.exists(path)]
        exit(1)

    for stats_dir in stats_paths:
        files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
        for path in files:
            try:
                IniFile(os.path.join(stats_dir, path)).validate(show_warnings=not args.no_warnings)
            except WZException, e:
                print e
