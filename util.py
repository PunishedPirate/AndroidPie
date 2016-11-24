#
# @author zhangyuwen1987@gmail.com
# @date   2016/10/09
#
import datetime
import os
import random
import re

NO_DIRECTORY_PATTERN = '(^.*/build/.*$)|(^.*/\.idea/.*$)|(^.*/build$)|(^.*/\.idea$)'


def camel_to_underline(camel_format):
    """
    驼峰命名格式转下划线命名格式
    """
    if not isinstance(camel_format, str):
        return camel_format

    underline_format = camel_format.lower()[0]
    for _s_ in camel_format[1:]:
        underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format


def underline_to_camel(underline_format):
    """
    下划线命名格式驼峰命名格式
    """
    if not isinstance(underline_format, str):
        return underline_format

    camel_format = ''
    for _s_ in underline_format.split('_'):
        camel_format += _s_.capitalize()
    return camel_format


def get_unique_number():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前时间
    random_num = random.randint(0, 100)  # 生成的随机整数n，其中0<=n<=100
    if random_num <= 10:
        random_num = str(0) + str(random_num)
    unique_num = str(now_time) + str(random_num)
    return unique_num


def filter_file_lines(src_path, line_pattern):
    dst_path = src_path + '.tmp'
    dst_file = open(dst_path, mode='w')
    for number, line in enumerate(open(src_path)):
        if re.search(line_pattern, line):
            yield number, line
            continue
        dst_file.writelines(line)
    dst_file.close()
    os.remove(src_path)
    os.rename(dst_path, src_path)


def replace_file_lines(src_path, line_pattern, old_string, new_string, *args):
    dic = dict()
    dic[old_string] = new_string
    while args and len(args) >= 2:
        dic[args[0]] = args[1]
        args = args[2:]

    for number, line, new_line in replace_file_lines_complex(src_path, line_pattern, **dic):
        yield number, line, new_line


def replace_file_lines_complex(src_path, line_pattern, **kwargs):
    dst_path = src_path + '.tmp'
    for number, line, new_line in generate_file_lines_complex(src_path, dst_path, line_pattern, **kwargs):
        yield number, line, new_line
    os.remove(src_path)
    os.rename(dst_path, src_path)


def generate_file_lines(src_path, dst_path, line_pattern, old_string, new_string, *args):
    dic = dict()
    dic[old_string] = new_string
    while args and len(args) >= 2:
        dic[args[0]] = args[1]
        args = args[2:]

    for number, line, new_line in generate_file_lines_complex(src_path, dst_path, line_pattern, **dic):
        yield number, line, new_line


def generate_file_lines_complex(src_path, dst_path, line_pattern, **kwargs):
    dst_file = open(dst_path, mode='w')
    for number, line in enumerate(open(src_path)):
        new_line = line
        if re.match(line_pattern, line):
            if kwargs:
                for key in kwargs:
                    new_line = new_line.replace(key, kwargs[key])
            yield number, line, new_line
        dst_file.writelines(new_line)
    dst_file.close()


def get_match_dirs(top_dir=os.getcwd(), yes_pattern='^.*/res$', no_pattern=None):
    for parent, dir_names, file_names in os.walk(top_dir):
        if re.match(NO_DIRECTORY_PATTERN, parent):
            continue
        if re.match(yes_pattern, parent):
            if no_pattern is None:
                yield parent
                continue
            if not re.match(no_pattern, parent):
                yield parent


def get_res_dirs(top_dir=os.getcwd()):
    for res_dir in get_match_dirs(top_dir, '^.*/res$'):
        yield res_dir


def get_match_paths(top_dir=os.getcwd(), yes_pattern='^.*\.xml$', no_pattern=None):
    for parent, dir_names, file_names in os.walk(top_dir):
        if re.match(NO_DIRECTORY_PATTERN, parent):
            continue
        for file_name in file_names:
            path = parent + os.sep + file_name
            if re.match(yes_pattern, path):
                if no_pattern is None:
                    yield path
                    continue
                if not re.match(no_pattern, path):
                    yield path


def get_build_gradle_paths(top_dir=os.getcwd()):
    for path in get_match_paths(top_dir, '^.*/build\.gradle$'):
        yield path


def get_path_relative_2_absolute(relative_path, root_dir=os.getcwd()):
    # root_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland'
    return root_dir + os.sep + relative_path


def get_res_dir(path):
    res_dir = re.search('.*/res', path)
    if res_dir:
        res_dir = res_dir.group()[:]
    return res_dir


def get_res_value_dir(res_dir, src_dimen):
    if src_dimen == 'default':
        return res_dir + os.sep + 'values'
    else:
        return res_dir + os.sep + 'values-' + src_dimen


def get_src_dimen(path):
    src_dimen = re.search('/values-.*dpi/', path)
    if src_dimen:
        src_dimen = src_dimen.group()[8:-1]
    else:
        src_dimen = re.search('/values/', path)
        if src_dimen:
            src_dimen = 'default'
    return src_dimen


def get_file_name(path):
    file_name = re.search('/[^/]*$', path)
    if file_name:
        file_name = file_name.group()[1:]
    return file_name


# 根据src_path所指向的*/res/layout/*.xml，以及src_dimen in ['default', 'hdpi', 'xhdpi', 'xxhdpi']
# 获得layout xml所对应的在src——dimen密度下面的dimen文件路径
def get_dst_dimen_xml_path(src_path, src_dimen):
    res_dir = get_res_dir(src_path)
    if not res_dir:
        return

    value_dir = get_res_value_dir(res_dir, src_dimen)

    src_name = get_file_name(src_path)
    dst_name = 'dimens_' + src_name
    dst_path = value_dir + os.sep + dst_name

    return dst_path


def main():
    print('Hello Python')

    project_dir = '/Users/zhangyuwen/Repository/Le/LetvGameCenter_Mainland'
    file_path = 'app/src/main/res/values-xhdpi/dimens_activity_first_meet.xml'

    src_path = project_dir + os.sep + file_path
    # for number, line in filter_file_line(src_path, '^</resources>$'):
    #     print(number, '-' * 10, line, sep='')

    # for res_dir in get_res_dirs(project_dir):
    #     print(res_dir)

    # src_path = project_dir + os.sep + file_path
    # dst_path = src_path + '.tmp'
    # for number, line, new_line in replace_file_lines(
    #         src_path, '^.*<dimen.*$', '<dimen', '<tricky', '</dimen', '</tricky'):
    #     print(number, WORD_YELLOW, ':', CLOSE,
    #           line.strip(), WORD_RED, '<' + '-' * 3 + '>', CLOSE, new_line.strip(), sep='')

    # for path in get_build_gradle_paths(project_dir):
    #     print(path)

    print(get_file_name(file_path))


if __name__ == '__main__':
    print('Hello Python', end='')
    main()
