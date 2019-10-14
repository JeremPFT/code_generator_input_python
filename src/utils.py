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

def compare_text(expected, actual):
    '''
    compare each line of given texts
    '''

    expected_lines = expected.split('\n')
    actual_lines   = actual.split('\n')

    for line_num in range(0, len(expected_lines)):
        if expected_lines[line_num] != actual_lines[line_num]:
            print("ERROR line %s" % (str(line_num)))
            print("expects '%s'" % (expected_lines(line_num)))
            print("got     '%s'" % (expected_lines(line_num)))

    print("matching texts")
