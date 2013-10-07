import os
from config_parser import WZConfigParser
from profile_loader import Profile, get_profiles_name_list


class WZException(Exception):
    pass


class IniFile(dict):
    profiles = get_profiles_name_list()

    def get_profile_for_ini(self):
        name = os.path.basename(self.path)[:-4]
        if name in self.profiles:
            return Profile(name)
        # hack for research
        elif name[:-5] in self.profiles:
            return Profile(name[:-5])
        else:
            raise WZException("Can't find profile for %s" % self.path)

    def __init__(self, path):
        self._warnings = {}
        self._errors = {}

        self.path = path
        self.profile = self.get_profile_for_ini()
        config = WZConfigParser()
        config.load(path)
        for section_name in config.sections():
            self[section_name] = dict(config.items(section_name))

    def _err(self, key, val):
        self._errors.setdefault(key, []).append('\t\t%s' % val)

    def _warn(self, key, val):
        self._warnings.setdefault(key, []).append('\t\t%s' % val)

    def validate(self, show_warnings=False):
        # clear prev result
        self._warnings = {}
        self._errors = {}

        for section_name, section in self.items():
            self.validate_section(section_name, section)

        print "validating %s(%s)" % (os.path.basename(self.path), self.path),  # string beginning
        if self._errors or show_warnings and self._warnings:
            if show_warnings:
                for key, val in self._warnings.items():
                    self._errors.setdefault(key, []).extend(val)
            print "... Failed. Has %s in %s sections" % ('errors or warnings' if show_warnings else "errors", len(self._errors))
            for key, error in self._errors.items():
                print "\t", key
                print '\n'.join(error)
        else:
            print "... OK"

    def validate_section(self, section_name, section):
        section_additional_keys = set(section.keys()).difference(set(self.profile.keys()))
        if section_additional_keys:
            self._err(section_name, 'has additional keys %s' % list(section_additional_keys))
        missed_keys = []

        for field_name in self.profile.keys():
            profile_data = self.profile[field_name]
            value = section.get(field_name)
            if value is None:
                if profile_data.get('required'):
                    missed_keys.append(field_name)
                continue
            elif value == str(profile_data.get('default')):  # int from ini came as str
                self._warn(section_name, 'default value: %s = %s' % (field_name, value))

            field_type = profile_data['type']

            if field_type == 'choice':
                if value.strip('"') not in profile_data['choices']:
                    self._err(section_name, 'wrong choice %s expect one of %s' % field_name, profile_data['choices'])
            elif field_type == 'boolean':
                if value not in ['0', '1']:
                    self._err(section_name, "wrong boolean value %s for %s" % (value, field_name))

        if missed_keys:
            self._err(section_name, 'missed keys %s' % list(missed_keys))
