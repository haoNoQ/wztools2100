try:
    # python 2
    from ConfigParser import ConfigParser
    from StringIO import StringIO
except ImportError:
    # python 3
    from configparser import ConfigParser
    from io import StringIO


class WZConfigParser(ConfigParser):
    """
    Extended ConfigParser
    Add handling space comments started from spaces.
    Save ini files on ini :)
    """

    def optionxform(self, optionstr):
        """default implementation makes it lowercase"""
        return optionstr

    def load(self, path):
        with open(path) as f:
            lines = f.readlines()
        is_header = True
        self.header = []
        new_lines = []
        for original_line in lines:
            line = original_line.strip()
            if line:
                if is_header:
                    if line.startswith(';'):
                        self.header.append(original_line.rstrip())
                    else:
                        is_header = False
                new_lines.append(line)
        fp = StringIO('\n'.join(new_lines))
        self.read_file(fp)

    def save(self, fp):
        if self.header:
            fp.write('\n'.join(self.header))
            fp.write('\n')
        self.write(fp)