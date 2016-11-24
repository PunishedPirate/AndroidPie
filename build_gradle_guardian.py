#
# @author zhangyuwen1987@gmail.com
# @date   2016/09/05
#

import os
import sys

from color_printer import CLOSE
from color_printer import WORD_GREEN
from color_printer import WORD_RED
from color_printer import WORD_YELLOW
from color_printer import print_blue
from util import get_build_gradle_paths
from util import replace_file_lines


def update_build_gradle_file_lines(old_string, new_string, root_dir=os.getcwd(), pattern=None):
    """
    找出当前目录下，所有build.gradle文件，并替换依赖库的版本号
    :param old_string:
    :param new_string:
    :param root_dir:
    :param pattern:
    :return:
    """
    if pattern is None:
        pattern = '.*(compile|provided).*:%s\'$' % old_string
    for path in get_build_gradle_paths(root_dir):
        show_file_path = False
        for number, line, new_line in replace_file_lines(path, pattern, old_string, new_string):
            print(WORD_YELLOW, '\tline', number, WORD_RED, line.strip(),
                  WORD_YELLOW, ' ==> ', WORD_RED, new_line.strip(), CLOSE)
            show_file_path = True
        if show_file_path:
            print_blue(path, '\n')


def main():
    for i in range(0, len(sys.argv)):
        print("param", i, sys.argv[i])

    if len(sys.argv) >= 3:
        update_build_gradle_file_lines(*sys.argv[1:])
    else:
        print(WORD_GREEN, 'Please input args:',
              WORD_RED, '(old_string, new_string, root_dir=os.getcwd(), '
                        'path_pattern="^build.gradle$", line_pattern=".*compile.*:[old_string]\'$"',
              CLOSE)
        print(CLOSE)


if __name__ == '__main__':
    main()
