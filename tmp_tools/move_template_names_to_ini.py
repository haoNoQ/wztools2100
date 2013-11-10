import os
import re
from ini_tools.enviroment import BASE_PATH, MP_PATH
from ini_tools import get_messages_strings_names_txt


def load_template(template_path, messages_strings_names_txt):
    with open(template_path) as f:
        text = f.read()
    expr = re.compile('\n\[(.*?)\]\n')

    def add_name(match):
        key = match.group(1)
        return '\n[%s]\nname=%s\n' % (key, messages_strings_names_txt[key])

    with open(template_path, 'w') as f:
        f.write(expr.sub(add_name, text))

if __name__ == '__main__':
    for path in [BASE_PATH, MP_PATH]:
        template_path = os.path.join(path, 'stats',  'templates.ini')
        load_template(template_path, get_messages_strings_names_txt(path))



