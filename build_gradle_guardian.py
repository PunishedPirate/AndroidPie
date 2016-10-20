#
#  @author zhangyuwen1987@gmail.com
# @date   2016/09/05
#

import os
import sys

import util
from color_printer import CLOSE
from color_printer import WORD_GREEN
from color_printer import WORD_RED
from color_printer import WORD_YELLOW
from color_printer import print_blue
from util import get_build_gradle_paths


def update_build_gradle_file_lines(old_string, new_string, root_dir=os.getcwd(), pattern=None):
    if pattern is None:
        pattern = '.*(compile|provided).*:%s\'$' % old_string
    for path in get_build_gradle_paths(root_dir):
        show_file_path = False
        for number, line, new_line in util.replace_file_lines(path, pattern, old_string, new_string):
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

        # update_build_gradle_file_line('23.2.0', '24.2.1', '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland')


if __name__ == '__main__':
    main()
