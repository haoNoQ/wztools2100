import os
from ini_file import IniFile, WZException
import argparse
from enviroment import ALL_PATHS


class ValidationResult(object):
    def __init__(self, path):
        self.errors = {}
        self.warnings = {}
        self.path = path

    def err(self, section_name, msg):
        self.errors.setdefault(section_name, []).append(msg)

    def warn(self, section_name, msg):
        self.warnings.setdefault(section_name, []).append(msg)

    def passed(self, show_warnings):
        return not (self.errors or show_warnings and self.warnings)

    def get_errors(self, show_warnings):
        result = []
        error_list = self.errors.copy()
        if show_warnings:
            for key, val in self.warnings.items():
                self.errors.setdefault(key, []).extend(val)
        result.append("... Failed. Has %s in %s sections" % ('errors or warnings' if show_warnings else "errors",
                                                             len(error_list)))
        for key, errors in error_list.items():
            result.append("\t%s" % key)
            result.append('\n'.join('\t\t%s' % err for err in errors))
        return '\n'.join(result)


def validate_section(init_file, section_name, section, result):
        section_additional_keys = set(section.keys()).difference(set(init_file.profile.keys()))
        if section_additional_keys:
            result.err(section_name, 'has additional keys %s' % list(section_additional_keys))
        missed_keys = []
        for field_name in init_file.profile.keys():
            profile_data = init_file.profile[field_name]
            value = section.get(field_name)
            if value is None:
                if profile_data.get('required'):
                    missed_keys.append(field_name)
                continue
            elif value == str(profile_data.get('default')):  # int from ini came as str
                result.warn(section_name, 'default value: %s = %s' % (field_name, value))

            field_type = profile_data['type']

            if field_type == 'choice':
                if value.strip('"') not in profile_data['choices']:
                    result.err(section_name, 'wrong choice %s expect one of %s' % field_name, profile_data['choices'])
            elif field_type == 'boolean':
                if value not in ['0', '1']:
                    result.err(section_name, "wrong boolean value %s for %s" % (value, field_name))
        if missed_keys:
            result.err(section_name, 'missed keys %s' % list(missed_keys))


def validate(ini_file, show_warnings=False):
        result = ValidationResult(ini_file.path)

        for section_name, section in ini_file.items():
            validate_section(ini_file, section_name, section, result)  # did we need ini file as argument

        print "validating %s(%s)" % (os.path.basename(ini_file.path), ini_file.path),  # string beginning

        if not result.passed(show_warnings):
            print result.get_errors(show_warnings)
        else:
            print "... OK"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-warnings', dest='no_warnings', action='store_true',
                        help="don't show warnings")
    args = parser.parse_args()

    stats_paths = [os.path.join(path, 'stats') for path in ALL_PATHS]
    if not all([os.path.exists(path) for path in stats_paths]):
        print "Invalid paths:", [path for path in stats_paths if not os.path.exists(path)]
        exit(1)

    for stats_dir in stats_paths:
        files = [path for path in os.listdir(stats_dir) if path.endswith('.ini')]
        for path in files:
            try:
                validate(IniFile(os.path.join(stats_dir, path)), show_warnings=not args.no_warnings)
            except WZException, e:
                print e
