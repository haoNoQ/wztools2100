import os
from ini_file import IniFile, WZException
from enviroment import BASE_PATH, MP_PATH
# hardcoded

pie_load_paths = ["structs/", "misc/", "effects/", "components/prop/", "components/weapons/", "components/bodies/",
                  "features/", "misc/micnum/", "misc/minum/", "misc/mivnum/", "misc/researchimds/"]


def _get_pies(folder_path):
        pie_paths = {}
        for path in pie_load_paths:
            result_path = os.path.join(folder_path, path)
            if not os.path.exists(result_path):  # mp does not have all folders
                continue
            for pie_path in os.listdir(result_path):
                if pie_path in pie_paths:
                    print "Has duplicate pie file names", '%s%s %s%s' % (path, pie_path, pie_paths[pie_path], pie_path)
                    continue
                pie_paths[pie_path] = path
        return pie_paths


def get_base_path():
    return _get_pies(BASE_PATH)


def get_mp_path():
    return _get_pies(MP_PATH)


def validate(stats_dir, pie_dict):
    stats_dir = os.path.join(stats_dir, 'stats')
    files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
    check_dict = pie_dict.copy()
    for path in files:
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
    return check_dict


if __name__ == '__main__':
    base = get_base_path()
    mp = get_mp_path()
<<<<<<< HEAD
    check_mp_intersect_base(base, mp)


    #parser = argparse.ArgumentParser()
    #parser.add_argument('stats_folders', help='list of folders with ini files', nargs='+')
    #parser.add_argument('--no-warnings', dest='no_warnings', action='store_true',
    #                    help="don't show warnings")
    #args = parser.parse_args()
    mp.update(base)

    unused_pies = (validate(BASE_PATH, base), validate(MP_PATH, mp))
    for key in unused_pies[0]:
        if key in unused_pies[1]:
            print "Unused key:", key




