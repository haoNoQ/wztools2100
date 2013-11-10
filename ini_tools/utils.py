import os
import sys
import string


def remove_c_style_comments(fd):
    """
    returns a list of strings which represent non-empty lines of file fd with all C-style comments eliminated
    """
    ret = []
    comment_state = False
    for line in fd:
        while True:
            # seems we have nothing left
            if len(line) < 2:
                break
            # we're still inside a comment
            if comment_state:
                idx = line.find("*/")
                if idx > -1:
                    line = line[idx + 2:]
                    comment_state = False
                    continue
                # comment doesn't seem to end on this line
                break
            # we're not inside any comment
            else:
                idx = line.find("/*")
                if idx > -1:
                    line = line[idx + 2:]
                    comment_state = True
                    continue
                if "//" in line:
                    line = line.split("//", 1)[0]
                # only now we can actually do our job
                line = line.strip()
                if len(line) > 0:
                    ret.append(line)
                break
    return ret

def get_messages_strings_names_txt(stats_path):
    messages_strings_names_txt = {}
    path = os.path.join(stats_path, "messages", "strings", "names.txt")
    if not os.path.isfile(path):
        print('Cant find names.txt inside %s' % stats_path)
        return {}
    with open(path) as fd:
        str_list = remove_c_style_comments(fd)

    if sys.hexversion >= 0x03000000:
        trans = str.maketrans("_()\"", "    ")
    else:
        trans = string.maketrans("_()\"", "    ")
    for line in str_list:
        one, two = line.split(None, 1)
        messages_strings_names_txt[one] = two.translate(trans).strip()
    return messages_strings_names_txt