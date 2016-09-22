#
#  @author zhangyuwen1987@gmail.com
# @date   2016/09/05
#

import os
import re
import sys

from print_color import *


def replace_file_line(old_string, new_string, root_dir=os.getcwd(), name_pattern=None, line_pattern=None):
    if name_pattern is None:
        name_pattern = '^build.gradle$'
    if line_pattern is None:
        line_pattern = '.*(compile|provided).*:%s\'$' % old_string

    for path in get_file_name_paths(root_dir, name_pattern):
        replace_file(path, old_string, new_string, line_pattern)


def get_file_name_paths(root_dir, name_pattern):
    for parent, dirNames, fileNames in os.walk(root_dir):
        for fileName in fileNames:
            if re.match(name_pattern, fileName):
                yield parent + os.sep + fileName


def replace_file(path, old_string, new_string, line_pattern):
    print(path)

    new_path = path + '.tmp'
    show_file_path = False
    for number, line, new_line in replace_string(path, new_path, old_string, new_string, line_pattern):
        print(WORD_YELLOW, '\tline', number, WORD_RED, line.strip(),
              WORD_YELLOW, ' ==> ', WORD_RED, new_line.strip(), CLOSE)
        show_file_path = True
    os.remove(path)
    os.rename(new_path, path)
    if show_file_path:
        print_blue(path, '\n')


def replace_string(in_path, out_path, old_string, new_string, line_pattern):
    out_file = open(out_path, 'w')

    for number, line in enumerate(open(in_path)):
        if re.match(line_pattern, line):
            new_line = line.replace(old_string, new_string)
            out_file.writelines(new_line)
            yield number, line, new_line
        else:
            out_file.writelines(line)

    out_file.close()


if __name__ == '__main__':
    for i in range(0, len(sys.argv)):
        print("param", i, sys.argv[i])

    if len(sys.argv) >= 3:
        replace_file_line(*sys.argv[1:])
    else:
        print(WORD_GREEN, 'Please input args:',
              WORD_RED, '(old_string, new_string, root_dir=os.getcwd(), '
                        'path_pattern="^build.gradle$", line_pattern=".*compile.*:[old_string]\'$"',
              CLOSE)
        print(CLOSE)

    # replace_file_line('23.3.0', '24.2.0', '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland')
