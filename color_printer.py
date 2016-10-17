#
# @author zhangyuwen1987@gmail.com
# @date   2016/09/06
#

WORD_BLACK = '\033[30m'
WORD_RED = '\033[31m'
WORD_GREEN = '\033[32m'
WORD_YELLOW = '\033[33m'
WORD_BLUE = '\033[34m'
WORD_PURPLE = '\033[35m'
WORD_SKY_BLUE = '\033[36m'
WORD_WHITE = '\033[37m'

REPR_BLACK = "\033[30m%s\033[0m"
REPR_RED = "\033[31m%s\033[0m"
REPR_GREEN = "\033[32m%s\033[0m"
REPR_YELLOW = "\033[33m%s\033[0m"
REPR_BLUE = "\033[34m%s\033[0m"
REPR_PURPLE = "\033[35m%s\033[0m"
REPR_SKY_BLUE = "\033[36m%s\033[0m"
REPR_WHITE = "\033[37m%s\033[0m"

CLOSE = '\33[0m'


def print_black(*args, **kwargs):
    print(WORD_BLACK, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_red(*args, **kwargs):
    print(WORD_RED, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_green(*args, **kwargs):
    print(WORD_GREEN, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_yellow(*args, **kwargs):
    print(WORD_YELLOW, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_blue(*args, **kwargs):
    print(WORD_BLUE, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_purple(*args, **kwargs):
    print(WORD_PURPLE, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_sky_blue(*args, **kwargs):
    print(WORD_SKY_BLUE, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


def print_white(*args, **kwargs):
    print(WORD_WHITE, sep='', end='')
    print(*args, **kwargs, end='')
    print(CLOSE)


if __name__ == '__main__':
    print_black('Hello Python', 'I like python')
    print_red('Hello Python', 'I like python')
    print_green('Hello Python', 'I like python')
    print_yellow('Hello Python', 'I like python')
    print_blue('Hello Python', 'I like python')
    print_purple('Hello Python', 'I like python')
    print_sky_blue('Hello Python', 'I like python')
    print_white('Hello Python', 'I like python')
