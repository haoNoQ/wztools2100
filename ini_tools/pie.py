from __future__ import print_function
import os
from .ini_file import IniFile
from .enviroment import BASE_PATH, MP_PATH


pie_load_paths = ["structs/", "misc/", "effects/", "components/prop/", "components/weapons/", "components/bodies/",
                  "features/", "misc/micnum/", "misc/minum/", "misc/mivnum/", "misc/researchimds/"]


def get_pies(folder_path):
        """
        Collect all pies from folder_path

        :param folder_path: path to root folder
        :type folder_path: str
        :return: dict of name, path to pie files
        :rtype: dict
        """
        pie_paths = {}
        errors = []
        for path in pie_load_paths:
            result_path = os.path.join(folder_path, path)
            if not os.path.exists(result_path):  # mp does not have all folders
                continue
            for pie_path in os.listdir(result_path):
                if pie_path in pie_paths:
                    errors.append("Has duplicate pie file names in %s: %s%s %s%s" % (folder_path, path, pie_path, pie_paths[pie_path], pie_path))
                    continue
                pie_paths[pie_path] = path
        return pie_paths, errors


def get_base_path():
    pies, errors = get_pies(BASE_PATH)
    errors and print(errors)
    return pies


def get_mp_path():
    pies, errors = get_pies(MP_PATH)
    errors and print(errors)
    return pies


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
                                print("missed pie", pie_item)
                        check_dict.pop(pie_item, None)
    return check_dict


if __name__ == '__main__':
    base = get_base_path()
    mp = get_mp_path()
    mp_only = mp.copy()
    mp.update(base)
    base_unused_pies = validate(BASE_PATH, base)
    mp_unused_pies = validate(MP_PATH, mp)

    print("Pie from BASE folder not mentioned in BASE stats")
    for k, v in sorted(base_unused_pies.items(), key=lambda x: x[1]):
        if k in mp_unused_pies:
            usage = 'Not used by BASE and MP'
        else:
            if k in mp_only:
                usage = "MP overrides this file"
            else:
                usage = "This file not used by BASE but used by MP"

        print('%s %s' % (os.path.join(v, k), usage))


    print("Pie from MP folders not mentioned in MP stats")
    for k, v in sorted(mp_unused_pies.items(), key=lambda x: x[1]):
        if k in mp_only:
            print('%s %s' % (os.path.join(v, k), 'Not used'))
