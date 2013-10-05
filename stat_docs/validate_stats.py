import os
from ini_file import IniFile, WZException


stats_paths = ['G:\\warzone2100\\data\\base\\stats', 'G:\\warzone2100\\data\\mp\\stats']




if __name__ == '__main__':
    for stats_dir in stats_paths:
        files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
        for path in files:
            try:
                IniFile(os.path.join(stats_dir, path)).validate(show_warnings=True)
            except WZException, e:
                print e
