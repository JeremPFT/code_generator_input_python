import ply.yacc as yacc

import project_parser_lexer
from project_parser_lexer import tokens

from model import Project, Package, Class, Subprogram

'''
project_def              : PROJECT_START project_name output_directory package_list PROJECT_STOP;
project_name             : IDENTIFIER;
IDENTIFIER               : [a-z][a-z0-9_];
output_directory         : quoted_string;
package_list             : NULL | package_list package_def;
package_def              : PACKAGE_START package_name dependance_list packageable_element_list PACKAGE_STOP;
package_name             : IDENTIFIER;
dependance_list          : NULL | dependance_list dependance_def;
packageable_element_list : NULL | packageable_element_list packageable_element_def;
packageable_element_def  : type_def | subprogram_def
'''

def p_project(p):
    'project : PROJECT_START IDENTIFIER output_directory package_list PROJECT_STOP'
    p[0] = Project(p[2], p[3], p[4])

def p_output_directory(p):
    'output_directory : OUTPUT_DIRECTORY STRING'
    p[0] = p[2]

def p_package_list_1(p):
    'package_list : '
    p[0] = []

def p_package_list_2(p):
    'package_list : package_list package_def'
    p[1].append(p[2])
    p[0] = p[1]

def p_package_def(p):
    'package_def : PACKAGE_START IDENTIFIER packageable_element_list PACKAGE_STOP'
    p[0] = Package(p[2], p[3])

def p_packageable_element_list_1(p):
    'packageable_element_list : '
    p[0] = []

def p_packageable_element_list_2(p):
    'packageable_element_list : packageable_element_list packageable_element'
    p[1].append(p[2])
    p[0] = p[1]

def p_packageable_element(p):
    '''packageable_element : class_definition
                           | subprogram_definition'''
    p[0] = p[1]

def p_class_definition(p):
    'class_definition : CLASS_START IDENTIFIER CLASS_STOP'
    p[0] = Class(p[2])

def p_subprogram_definition(p):
    'subprogram_definition : SUBPROGRAM IDENTIFIER'
    p[0] = Subprogram(p[2], [])

def p_error(p):
    if p == None:
        print("Error: end of file")
        return

    print("Syntax error in input!")
    message = "line "
    message += str(p.lineno)
    message += ": unexpected "
    message += str(p.type)
    # message += " " + str(p)
    print(message)

parser = yacc.yacc()

def test_grammar():
    data = '''project a_project_name
output_directory "d:/Users/jpiffret/AppData/Roaming/Dropbox/projets_perso/ada/code_generator_input/examples/model"
    package pkg_1_name
        class pkg_1_cls_1_name end_class
        class pkg_1_cls_2_name end_class
        subprogram pkg_1_subprg_1_name
    end_package
    package pkg_2_name
        class pkg_2_cls_1_name end_class
        class pkg_2_cls_2_name end_class
    end_package
end_project
    '''

    result = parser.parse(data)
    if result != None:
        print(result)

if __name__ == '__main__':
    test_grammar()
