import os

def dbg(str):
    print(str)


class indent:
    shift = 2
    value = 0

    @staticmethod
    def str():
        return indent.value * " "

    @staticmethod
    def incr():
        indent.value += indent.shift

    @staticmethod
    def decr():
        indent.value -= indent.shift


def capitalize_identifier(identifier):
    orig_list = identifier.split("_")
    result_list = []
    for str in orig_list:
        result_list.append(str.capitalize())
    return '_'.join(result_list)


def build_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
