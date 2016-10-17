#
# @author zhangyuwen1987@gmail.com
# @date   2016/10/05
#

import os
import re
import sys

from color_printer import *
from dimen_transformer import transform_single_dimen_xml
from util import camel_to_underline, filter_file_lines, get_res_dirs, get_path_relative_2_absolute, \
    get_dst_dimen_xml_path

# 需要检查的属性，若这些属性存在，并且设置了响应的dp值，则需要进行机型适配
attr_dict = {'View': ['layout_width=', 'layout_height=',
                      'padding=', 'paddingLeft=', 'paddingTop=', 'paddingRight=', 'paddingBottom=',
                      'margin=', 'marginLeft=', 'marginTop=', 'marginRight=', 'marginBottom=',
                      'marginStart=', 'marginEnd='],
             'TextView': ['textSize='],
             'stroke': [':width='],
             'corners': [':radius=',
                         ':topLeftRadius=', ':topRightRadius=', ':bottomLeftRadius=', ':bottomRightRadius='],
             'item': [':left=', ':top=', ':right=', ':bottom=']}

# 为新生成的dimen资源，取一个合适的名字，取名规则：name = name_dict[key] + attr_dict[key][i]
name_dict = {'View': [':id=', ':background='],
             'ImageView': [':src='],
             'TextView': [':text=']}

# 为做不同密度屏幕的适配，记录1dp=xpx的换算关系表
dimen_dict = {'hdpi': 1.5, 'xhdpi': 2.0, 'xxhdpi': 3.0}


class Node:
    def __init__(self):
        self.attr_map = {}
        self.attr_list = []
        self.label = None
        self.name = None

    def add(self, line, key, value):
        self.attr_map[key] = value
        self.attr_list.append((line, key, value))

    def set_label(self, label):
        self.label = label

    def set_name(self, name):
        if self.name is None:
            self.name = name

    def get_attr_name(self):
        if self.name:
            return get_words(self.name, r'[A-Za-z0-9]+')
        self.name = camel_to_underline(self.label)
        for line, key, value in self.attr_list:
            self.name += '_' + str(line)
        return self.name

    def get_res_name(self, attr):
        return self.get_attr_name() + '_' + attr


def filter_node_list(func):
    def wrapper(src_path):
        g = func(src_path)
        try:
            while True:
                node = next(g)
                if len(node.attr_list) == 0:
                    continue
                yield node
        except StopIteration:
            return None

    return wrapper


# parse一个layout xml，获得label，name（唯一，用于生成dimen资源的名字），attr, attr_value
@filter_node_list
def parse_source_xml(src_path):
    node = None
    for number, line in enumerate(open(src_path)):
        number += 1

        # 0.尝试获得label
        label = get_label(line)
        if label:
            node = Node()
            node.set_label(label)
            attr_list = get_attr_list(label)

        if node is None:
            continue

        # 1.尝试获得需要适配的attr, attr_value
        for attr in attr_list:
            if re.search(attr, line) is None:
                continue

            attr_value = re.search('=\"(\d|\.)+(dp|sp)\"', line)
            if attr_value:
                node.add(number, get_words(attr), attr_value.group()[2:-1])
            break

        # 2.尝试获得name
        name = get_name(node.label, line)
        if name:
            node.set_name(name)

        # 3.尝试获得label结束标志
        end = re.search('>|//>', line)
        if end:
            yield node
            node = None


# TODO: optimize, 是否可以一边parse，一遍写文件吗？
def rewrite_source_xml(src_path):
    g = parse_source_xml(src_path)
    node = get_node(g)
    if node is None:
        return

    src_file = open(src_path)
    dst_path = src_path + '.tmp'
    dst_file = open(dst_path, mode='w')
    attr_no = 0
    line_number, attr_name, attr_value = node.attr_list[attr_no]
    for num, line in enumerate(src_file):
        if num != line_number:
            dst_file.writelines(line)
        else:
            line = line.replace(attr_value, '@dimen/' + node.get_res_name(attr_name))
            dst_file.writelines(line)
            attr_no += 1
            if attr_no >= len(node.attr_list):
                node = get_node(g)
                attr_no = 0
            if node:
                line_number, attr_name, attr_value = node.attr_list[attr_no]
    src_file.close()
    os.remove(src_path)
    os.rename(dst_path, src_path)


def get_node(g):
    try:
        node = next(g)
        return node
    except StopIteration:
        return None


# 为一个layout xml创建标准的dimen resource xml
def create_dimen_xml(src_path, src_dimen='hdpi'):
    g = parse_source_xml(src_path)
    node = get_node(g)
    if node is None:
        return

    dst_path = get_dst_dimen_xml_path(src_path, src_dimen)

    # 如果dst_path已经存在，则需要将新生成的dimen资源append在文件合适的位置
    if os.path.exists(dst_path):
        for number, line in filter_file_lines(dst_path, '^</resources>$'):
            print('filter line ', WORD_YELLOW, number, CLOSE, ': ', WORD_RED, line.strip(), CLOSE, sep='')
    else:
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        with open(dst_path, mode='w') as f:
            f.writelines('<resources>\n')

    with open(dst_path, mode='a') as dst_file:
        while node:
            dst_file.writelines('    <!-- ' + node.label + ': ' + node.get_attr_name() + ' -->\n')
            for key in node.attr_map:
                value = node.attr_map[key]
                line = '    <dimen name="' + node.get_res_name(key) + '">' + value + '</dimen>\n'
                dst_file.writelines(line)
            dst_file.writelines('\n')
            node = get_node(g)
        dst_file.writelines('</resources>')
    return dst_path


def adapt_xmls(root_dir=os.getcwd(), src_dimen='xhdpi', *dst_dimens):
    for res_dir in get_res_dirs(root_dir):
        layout_dir_list = [(res_dir + os.sep + name) for name in ('layout', 'drawable')]
        for layout_dir in layout_dir_list:
            for parent, dir_names, file_names in os.walk(layout_dir):
                for file_name in file_names:
                    src_path = layout_dir + os.sep + file_name
                    adapt_single_xml(src_path, src_dimen, *dst_dimens)


def adapt_single_xml_relatively(src_path, src_dimen='xhdpi', *dst_dimens):
    src_path = get_path_relative_2_absolute(src_path)
    adapt_single_xml(src_path, src_dimen, *dst_dimens)


def adapt_single_xml(src_path, src_dimen='xhdpi', *dst_dimens):
    test_parse_source_xml(src_path)
    create_dimen_xml(src_path, src_dimen)
    rewrite_source_xml(src_path)
    if not dst_dimens:
        dst_dimens = ('hdpi',)

    src_dimen_xml = get_dst_dimen_xml_path(src_path, src_dimen)
    if os.path.exists(src_dimen_xml):
        transform_single_dimen_xml(src_dimen_xml, *dst_dimens)


def slice(start, end, step=1):
    def wrapper1(method):
        def wrapper2(*args, **kwargs):
            val = method(*args, **kwargs)
            if val:
                return val[start:end:step]

        return wrapper2

    return wrapper1


# 处理字符串，过滤出所有符合pattern的字符串，以下划线拼接起来
def get_words(string, pattern=r'[A-Za-z]+'):
    if string is None:
        return None
    words = []
    p = re.compile(pattern)
    for m in p.finditer(string):
        words.append(m.group())
    return '_'.join(words)


def filter_words(func):
    def wrapper(*args):
        return get_words(func(*args))

    return wrapper


@filter_words
def get_label(line):
    label = re.search('<\w+\s', line)
    if label:
        # 找到当前行的标签，根据标签，找到需要检查的属性表
        return label.group()[:]


def get_attr_list(label):
    attr_list = attr_dict.get('View')
    if label in attr_dict:
        attr_list = attr_dict.get(label) + attr_list
    return attr_list


@slice(2, -1)
def get_name(label, line):
    name_list = name_dict.get('View')
    if label in name_dict:
        name_list = name_list + name_dict.get(label)

    for name in name_list:
        if re.search(name, line) is None:
            continue
        name_value = re.search('=\"@\+?\w*/\w*\"', line)
        if name_value is None:
            continue
        return name_value.group()


def test_parse_source_xml(src_path):
    # for test
    print(src_path)
    node_count = 0
    attr_count = 0
    for node in parse_source_xml(src_path):
        node_count += 1
        print(WORD_RED, node.label, CLOSE, '-' * 8, WORD_RED, node.name, CLOSE, sep='')
        for tup in node.attr_list:
            attr_count += 1
            print(WORD_GREEN, tup[0], ':', tup[1], CLOSE, WORD_RED, '=>', CLOSE, WORD_BLUE, tup[2], CLOSE, sep='')
        print()
    if node_count != 0:
        print(WORD_YELLOW, 'node_count:', node_count, 'attr_count:', attr_count, CLOSE)


def main():
    if len(sys.argv) <= 1:
        return
    func_name = sys.argv[1]
    if func_name == 'adapt_single_xml':
        adapt_single_xml_relatively(*sys.argv[2:])
        return

    if func_name == 'adapt_xmls':
        print(sys.argv[2:])
        print(*sys.argv[2:])
        adapt_xmls(os.getcwd(), *sys.argv[2:])

    print('This is for testing....')
    # res_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland/app/src/main/res'
    # layout_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland/app/src/main/res/layout'
    # file_name = 'activity_beauty_memory.xml'
    # src_path = layout_dir + os.sep + file_name

    # test_parse_source_xml(src_path)
    # create_standard_xml(res_dir, layout_dir, file_name)
    # rewrite_source_xml(src_path)

    # root_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland'
    # adapt_xmls(root_dir, 'xhdpi', 'xxhdpi')

    # print(get_words(':layout_marginRight='))

    # src_path = 'app/src/main/res/drawable/dialog_default_title_bg.xml'
    # adapt_single_xml_relatively(src_path)


if __name__ == '__main__':
    for i in range(len(sys.argv)):
        print("参数", i, sys.argv[i])

    main()
