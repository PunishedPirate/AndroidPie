#
# @author zhangyuwen1987@gmail.com
# @date   2016/08/31
#

import os
import re
import sys

from color_printer import *
from util import get_res_dirs, get_res_value_dir, get_file_name, get_res_dir, get_src_dimen, \
    get_path_relative_2_absolute

dimen_dict = {'default': 1.5, 'hdpi': 1.5, 'xhdpi': 2.0, 'xxhdpi': 3.0}


def get_dimen(key):
    return dimen_dict.get(key, 1.0)


def generate_single_xml(src_path, dst_path, scale,
                        line_pattern='.*<dimen.*\">.*<\/dimen>.*',
                        name_pattern='=\".*\">',
                        dimen_pattern='>.*<'):
    modified = False
    dst_file = open(dst_path, mode='w')
    for number, line in enumerate(open(src_path)):
        if re.match(line_pattern, line):
            name_obj = re.search(name_pattern, line)
            if name_obj:
                dimen_obj = re.search(dimen_pattern, line)
                if dimen_obj:
                    name = name_obj.group()[2:-2]
                    org_dimen = dimen_obj.group()[1:-3]
                    cur_dimen = str(round(float(org_dimen) * scale, 2))
                    src_dp = dimen_obj.group()[1:-1]
                    dst_dp = cur_dimen + dimen_obj.group()[-3:-1]
                    yield number, line, name, src_dp, dst_dp
                    line = line.replace(org_dimen, cur_dimen)
                    modified = True
        dst_file.writelines(line)
    dst_file.close()
    return modified


# 当src_path所代表的xml，不含有dimens资源时，不需要生成此文件
def generate_single_dimen_xml(src_path, dst_path, scale):
    g = generate_single_xml(src_path, dst_path, scale)
    try:
        while True:
            number, line, name, src_dp, dst_dp = next(g)
            print(number, ':\t', line.strip(), '\t',
                  WORD_GREEN, name, '\t',
                  WORD_RED, src_dp, WORD_YELLOW, '\t=>\t', WORD_RED, dst_dp, CLOSE, sep='')
    except StopIteration as e:
        if not e.value:
            os.remove(dst_path)


def transform_dimen_xmls(src_suffix, src_dimen, dst_suffix, dst_dimen, root_dir=os.getcwd()):
    for res_dir in get_res_dirs(root_dir):
        src_dir = get_res_value_dir(res_dir, src_suffix)
        if not os.path.exists(src_dir):
            continue

        print(res_dir, CLOSE, sep='')
        scale = float(src_dimen) / float(dst_dimen)
        print(WORD_YELLOW, '%s => %s\t scale:%s' % (src_suffix, dst_suffix, scale), CLOSE, sep='')

        for parent, dir_names, file_names in os.walk(src_dir):
            for file_name in file_names:
                if not re.match('.*\.xml$', file_name):
                    continue
                src_path = src_dir + os.sep + file_name
                dst_dir = res_dir + os.sep + 'values-' + dst_suffix
                if not os.path.exists(dst_dir):
                    os.mkdir(dst_dir)
                dst_path = dst_dir + os.sep + file_name
                print(WORD_BLUE, src_path, CLOSE, sep='')
                generate_single_dimen_xml(src_path, dst_path, scale)


def transform_single_dimen_xml_relatively(src_path, *transform_dimens):
    src_path = get_path_relative_2_absolute(src_path)
    transform_single_dimen_xml(src_path, *transform_dimens)


def transform_single_dimen_xml(src_path, *transform_dimens):
    if re.match('.*\.xml$', src_path) is None:
        return

    if os.path.isfile(src_path) is None:
        return

    src_dimen = get_src_dimen(src_path)
    if src_dimen is None:
        return

    res_dir = get_res_dir(src_path)
    if res_dir is None:
        return

    file_name = get_file_name(src_path)
    if file_name is None:
        return

    for dst_dimen in transform_dimens:
        dst_dir = get_res_value_dir(res_dir, dst_dimen)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        dst_path = dst_dir + os.sep + file_name
        scale = float(get_dimen(src_dimen)) / float(get_dimen(dst_dimen))
        generate_single_dimen_xml(src_path, dst_path, scale)


def main():
    for i in range(len(sys.argv)):
        print("参数", i, sys.argv[i])

    if len(sys.argv) <= 1:
        return

    title = 'Auto Dimen Transformer'
    print(WORD_YELLOW, title.center(100, '-'), CLOSE, sep='')

    func_name = sys.argv[1]
    if func_name == 'transform_single_dimen_xml':
        transform_single_dimen_xml(*sys.argv[2:])
        return

    if func_name == 'transform_dimen_xmls':
        transform_dimen_xmls(*sys.argv[2:])
        return

    print('Please input 1, 2, 4 or 5 arguments!')

    # project_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland'
    # res_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland/app/src/main/res'
    # layout_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland/app/src/main/res/layout'
    # file_name = 'activity_beauty_memory.xml'
    # src_path = layout_dir + os.sep + file_name

    # relative_path = 'app/src/main/res/values-xhdpi/dimens.xml'
    # src_path = project_dir + os.sep + relative_path
    # transform_single_dimen_xml(src_path, 'xxhdpi')
    # transform_dimen_xmls('default', 1.5, 'xxhdpi', 3.0, project_dir)

    # project_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland'
    # relative_path = 'app/src/main/res/values/dimens.xml'
    # src_path = project_dir + os.sep + relative_path
    # transform_single_dimen_xml(src_path, 'xxhdpi')


if __name__ == '__main__':
    main()
