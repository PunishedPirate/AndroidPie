#
# @author zhangyuwen1987@gmail.com
# @date   2016/08/31
#

import sys
import os
import re
from print_color import *


# 获得某个文件目录下面,匹配yes_pattern, 但不匹配no_pattern的文件夹路径
def get_parent_paths(root_dir=os.getcwd(), yes_pattern='.*res$', no_pattern='.*build.*'):
    for parent, dirNames, fileNames in os.walk(root_dir):
        if re.match(yes_pattern, parent) and not re.match(no_pattern, parent):
            yield parent


def transform_dimen(src_path, dst_path, scale,
                    line_pattern='.*<dimen.*\">.*<\/dimen>.*',
                    name_pattern='=\".*\">',
                    dimen_pattern='>.*<'):
    dst_file = open(dst_path, mode='w')

    for line in open(src_path):
        if re.match(line_pattern, line):
            name_obj = re.search(name_pattern, line)
            if name_obj:
                dimen_obj = re.search(dimen_pattern, line)
                if dimen_obj:
                    name = name_obj.group()[2:-2]
                    org_dimen = dimen_obj.group()[1:-3]
                    cur_dimen = str(round(float(org_dimen) * scale, 2))
                    line = line.replace(org_dimen, cur_dimen)
                    yield name, dimen_obj.group()[1:-1], cur_dimen + dimen_obj.group()[-3:-1]
        dst_file.writelines(line)
    dst_file.close()


def auto_transform_dimen(src_suffix, src_dimen, dst_suffix, dst_dimen, root_dir=os.getcwd()):
    for parent_path in get_parent_paths(root_dir):
        src_path = parent_path + os.sep + 'values-' + src_suffix + os.sep + 'dimens.xml'
        dst_path = parent_path + os.sep + 'values-' + dst_suffix + os.sep + 'dimens.xml'
        if not os.path.exists(src_path):
            continue
        scale = float(src_dimen) / float(dst_dimen)
        print(WORD_BLUE, parent_path, CLOSE)
        print(WORD_YELLOW, '%s => %s\tscale:%s' % (src_suffix, dst_suffix, scale), CLOSE)

        for name, old_dimen, new_dimen in transform_dimen(src_path, dst_path, scale):
            print(WORD_GREEN, name,
                  WORD_RED, old_dimen, WORD_YELLOW, ' => ', WORD_RED, new_dimen,
                  CLOSE)
        print()


if __name__ == '__main__':
    for i in range(len(sys.argv)):
        print("参数", i, sys.argv[i])

    title = 'Auto Dimen Transformer'
    print(WORD_YELLOW, title.center(100, '-'), CLOSE, sep='')
    if len(sys.argv) >= 5:
        auto_transform_dimen(*sys.argv[1:])
    else:
        print(
            WORD_RED, 'please input args:\t', '(src_suffix, src_dimen, dst_suffix, dst_dimen)\n',
            WORD_RED, 'something like: \t',
            WORD_GREEN, '(hdpi, 1.5, xhdpi, 2.0)',
            CLOSE, sep='')

    # auto_transform_dimen('hdpi', 1.5, 'xhdpi', 2.0, '/Users/zhangyuwen/Repository/gerrit/Le/LetvStoreInternational')
    # string_line = '    <dimen name="tv_convenient_way_hint_margin_top">20dp</dimen>'
    # pattern = '=\".*\">'
    # search_obj = re.search(pattern, string_line)
    # print(search_obj.group())
