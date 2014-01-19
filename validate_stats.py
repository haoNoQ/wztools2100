#!/usr/bin/python3

from __future__ import print_function
import os
import argparse
from ini_tools import IniFile, get_pies


class Validator(object):
    ERROR, WARNING = 1, 2

    def add_section(self, name):
        self.messages.append([name, []])

    def err(self, header, text):
        self.messages[-1][1].append([self.ERROR, header, text])

    def warn(self, header, text):
        self.messages[-1][1].append([self.WARNING, header, text])

    def __init__(self, mod_folder, base_path, show_warnings=True):
        self.messages = []

        stats_dir = os.path.join(mod_folder, 'stats')


        self.pies, errors = get_pies(base_path) # load base pies

        if mod_folder != base_path:
            mod_pies, errors = get_pies(mod_folder)
            self.pies.update(mod_pies)

        if errors:
            self.add_section("Pie errors")
            [self.err("Pie missed", err) for err in errors]
        self.show_warnings = show_warnings

        self.ini_files = {}
        files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
        for path in files:
            ini_file = IniFile(os.path.join(stats_dir, path))
            self.ini_files[ini_file.name] = ini_file

    def validate(self):
        for ini_file in self.ini_files.values():
            self.add_section('File: %s (%s)' % (ini_file.name, ini_file.path))
            self.validate_file(ini_file)
        self.print_error_message()

    def validate_file(self, ini_file):
        for section_name in ini_file:
            self.validate_section(ini_file, section_name)

    def validate_section(self, ini_file, section_name):
        section = ini_file[section_name]

        # check keys present in section and missed in profile
        section_additional_keys = set(section.keys()).difference(set(ini_file.profile.keys()))
        if section_additional_keys:
            self.err(section_name, 'has additional keys %s' % list(section_additional_keys))

        missed_keys = []
        for field_name in ini_file.profile.keys():
            profile_field = ini_file.profile[field_name]
            value = section.get(field_name)
            if value is None:
                if profile_field.get('required'):
                    missed_keys.append(field_name)
                continue
            elif value == str(profile_field.get('default')):  # int from ini came as str
                self.warn(section_name, 'default value: %s = %s' % (field_name, value))

            # validate by field type
            field_type = profile_field['type']
            if field_type == 'choice':
                if value.strip('"') not in profile_field['choices']:
                    self.err(section_name, 'wrong choice "%s = %s" expect one of %s' % (field_name, value, profile_field['choices']))
            elif field_type == 'boolean':
                if value not in ['0', '1']:
                    self.err(section_name, "wrong boolean value %s for %s" % (value, field_name))
            elif field_type == 'pie':
                vals = [x.strip() for x in value.split(',')]
                for val in vals:
                    if val !='0' and val.lower() not in self.pies:
                        self.err(section_name, 'Missed pie "%s" for field %s' % (val, field_name))
                    else:
                        if val not in self.pies:
                            self.warn(section_name, 'Pie name "%s" did not match exactly with file for field %s' % (value, field_name))
            elif field_type in ['key', 'key_list']:
                reference_list = ini_file.profile.get_reference_keys(field_name)
                keys = value.strip().split(',')

                def key_in_reference(key, reference_list):
                    for reference_name in reference_list:
                        if reference_name.startswith('research'):
                            reference_source = ini_file
                        else:
                            if reference_name in self.ini_files:
                                reference_source = self.ini_files[reference_name]
                            else:
                                continue
                        if key in reference_source:
                            return True

                for key_id in keys:
                    if key_in_reference(key_id.strip(), reference_list):
                        continue
                    self.err(section_name, "key <%s> in filed <%s> is missed for section <%s>" % (key_id,
                                                                                                  field_name,
                                                                                                  section_name))
        if missed_keys:
            self.err(section_name, 'missed keys %s' % list(missed_keys))

    def print_error_message(self):
        result = []

        max_header_length = 0

        for __, values in self.messages:
            for __, header, __ in values:
                max_header_length = max(len(header), max_header_length)

        for section_name, values in self.messages:
            error_types = self.show_warnings and [self.ERROR, self.WARNING] or [self.ERROR]
            values = [x for x in values if x[0] in error_types]  # remove warnings
            if not values:
                continue
            result.append('%s, number of %s: %s' % (section_name,
                                                    self.show_warnings and 'errors and warnings' or 'errors',
                                                    len(values)))
            for err_type, header, text in values:
                template = '\t%-{0}s  %s'.format(max_header_length)
                result.append(template % (header, text))
        print("\n".join(result))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('modpath', metavar='<modpath>', help='path to mod folder')
    parser.add_argument('basepath', metavar='<basepath>', help='path to base folder')

    parser.add_argument('--no-warnings', dest='no_warnings', action='store_true',
                        help="don't show warnings")
    args = parser.parse_args()

    mod_path = args.modpath
    base_path = args.basepath

    if not os.path.exists(mod_path):
        print("Invalid mod path:%s" % mod_path)
        exit(1)
    if not os.path.exists(base_path):
        print("Invalid base path:%s" % base_path)
        exit(1)

    validator = Validator(mod_path, base_path, show_warnings=not args.no_warnings)
    validator.validate()

