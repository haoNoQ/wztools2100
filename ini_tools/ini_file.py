import os
from config_parser import WZConfigParser
from profile_loader import Profile, get_profiles_name_list
from generate_ini_header import get_header


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

    def __init__(self, path, data_dict=None):
        self.path = path
        self.name = os.path.basename(path)[:-4]
        self.profile = self.get_profile_for_ini()
        if data_dict:
            self.update(data_dict)
        else:
            config = WZConfigParser()
            config.load(path)
            for section_name in config.sections():
                self[section_name] = dict(config.items(section_name))

    def save(self, filename=None):
        if filename is None:
            filename = self.path
        text_list = [get_header(self.profile)]
        for section_name, section_items in self.items():
            section_list = ['', '[%s]' % section_name]
            for item in sorted(section_items.items(),  key=lambda x: self.profile.field_order.index(x[0])):
                prepared_value = self.prepare_value(item)
                if prepared_value:
                    section_list.append(prepared_value)
            text_list.extend(section_list)
        with open(filename, 'w') as fd:
            fd.write('\n'.join(text_list))

    def prepare_value(self, item):
        key, val = item
        field = self.profile[key]
        if str(field.get('default')) == str(val):
            return None
        if field['type'] == 'pie':
            return "%s = %s" % (key, val.lower())
        return "%s = %s" % item


#if __name__ == '__main__':
#    ini_file = IniFile("G:/warzone2100/data/base/stats/propulsion.ini")
#    with open('tmp.ini', 'w') as fd:
#        ini_file.save(fd)

    @classmethod
    def from_dict(cls, data_dict, dest_file):
        return IniFile()