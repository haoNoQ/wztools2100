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
