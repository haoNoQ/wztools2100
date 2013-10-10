import os
from ini_file import IniFile, WZException

# hardcoded
base_path = 'g:/warzone2100/data/base'
mp_path = 'g:/warzone2100/data/mp'

pie_load_paths = ["structs/", "misc/", "effects/", "components/prop/", "components/weapons/", "components/bodies/",
                  "features/", "misc/micnum/", "misc/minum/", "misc/mivnum/", "misc/researchimds/"]

def _get_pies(base_path):

        pie_paths = {}
        for path in pie_load_paths:
            result_path = os.path.join(base_path, path)
            if not os.path.exists(result_path):  # mp does not have all folders
                continue
            for pie_path in os.listdir(result_path):
                if pie_path in pie_paths:
                    print "Has duplicate pie file names", '%s%s %s%s' % (path, pie_path, pie_paths[pie_path], pie_path)
                    continue
                pie_paths[pie_path] = path
        return pie_paths


def get_base_path():
    return _get_pies(base_path)


def get_mp_path():
    return _get_pies(mp_path)


def check_mp_intersect_base(base, mp):
    for key in mp:
        if key in base:
            print "MP has same pie file as base. base: %s mp: %s" % (os.path.join(base[key], key), os.path.join( mp[key], key))

if __name__ == '__main__':
    base = get_base_path()
    mp = get_mp_path()
    check_mp_intersect_base(base, mp)


    #parser = argparse.ArgumentParser()
    #parser.add_argument('stats_folders', help='list of folders with ini files', nargs='+')
    #parser.add_argument('--no-warnings', dest='no_warnings', action='store_true',
    #                    help="don't show warnings")
    #args = parser.parse_args()
    mp.update(base)
    stats_data = [('g:/warzone2100/data/base/stats', base), ('g:/warzone2100/data/mp/stats', mp)]
    if not all([os.path.exists(path[0]) for path in stats_data]):
        print "Invalid paths:", [path[0] for path in stats_data if not os.path.exists(path)]
        exit(1)

    unused_pie = []
    for stats_dir, pie_dict in stats_data:
        files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
        check_dict = pie_dict.copy()
        unused_pie.append(check_dict)
        for path in files:
            try:
                ini_file = IniFile(os.path.join(stats_dir, path))
                for section_name, section in ini_file.items():
                    for field_name, profile_data in ini_file.profile.items():
                        if profile_data.get('type') == 'pie':
                            pies = [x.strip().lower() for x in section.get(field_name, '').split(',') if x]
                            for pie_item in pies:
                                if not pie_item in pie_dict:
                                    #hack
                                    if not pie_item == '0':
                                        print "missed pie", pie_item
                                check_dict.pop(pie_item, None)

            except WZException, e:
                print e

    for key in unused_pie[0]:
        if key in unused_pie[1]:
            print key



