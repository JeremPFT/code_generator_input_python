''' Utilities functions.

- dbg
Output given string

- indent (class)
Indent output code.

- capitalize_identifier
Capitalize first letter and each letter following a '_'

- directory
Normalize directory

- rmdir
Delete directory

- build_dir
Create recursively directory

- dir_exists
Return True if directory exists

- text_files_match
Return True if 2 files are the same

- assert_no_empty_string

- assert_type

- build_list_image
Use indent
'''

import os
import shutil

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


def directory(path):
    'normalize given path and replace ~/ with HOME path'

    result = os.path.normpath(path)
    if result.startswith("~\\"):
        home = os.path.normpath(os.environ["HOME"])
        result = os.path.join(home, result[2:])
    return result

def rmdir(path):
    shutil.rmtree(directory(path))

def build_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def dir_exists(path, name):
    path = os.path.normpath(path)
    if not os.path.exists(path):
        print("ERROR: %s doesn't exist : %s" % (name, path))
        return False
    else:
        print("path %s exists : %s" % (name, path))
        return True

def text_files_match(expected, obtained):
    '''
    compare each line of given texts
    '''

    dbg("%s expected: %s, obtained: %s" % (text_files_match.__name__,
                                           expected,
                                           obtained))

    expected_lines = open(directory(expected), "r").read().split('\n')
    obtained_lines = open(directory(obtained), "r").read().split('\n')

    error_msg = ""
    for line_num in range(0, len(expected_lines)):
        expected_line = expected_lines[line_num]
        obtained_line = obtained_lines[line_num]
        if expected_line != obtained_line:
            error_msg = 'ERROR line ' + str(line_num) + '\n' \
                + 'expects "' + expected_line + '"\n' \
                + 'got     "' + obtained_line + '"'
            print(error_msg)

    if error_msg == "":
        print("matching files\n%s\n%s" % (expected, obtained))
        return True
    else:
        return False

def assert_no_empty_string(value):
    assert type(value) == str, \
        "given value is not a string {!r}".format(value)
    assert value != "", \
        "given string is empty"

def assert_type(value, type):
    msg = "given value is not a {!s}: {!r} is {!s}"
    msg = msg.format(type, value, type(value))

    if type.__name__ == "bool":
        assert value == False or value == True, msg
    else:
        assert type(value) == type, msg

def build_list_image(list):
    image = ""
    indent.incr()
    for item in list:
        image += indent.str() + str(item)
        if item != list[-1]:
            image += '\n'
    indent.decr()
    return image
