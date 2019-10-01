import ply.yacc as yacc

import project_parser_lexer
from project_parser_lexer import tokens

from model import Project, Package, Class, Subprogram, Procedure, Function, Parameter

'''
project                  : PROJECT_START IDENTIFIER output_directory package_list PROJECT_STOP
output_directory         : quoted_string
package_list             : <empty> | package_list package_def
package_def              : PACKAGE_START IDENTIFIER dependance_list packageable_element_list PACKAGE_STOP
dependance_list          : <empty> | dependance_list dependance_def
dependance_def           : WITH IDENTIFIER
packageable_element_list : <empty> | packageable_element_list packageable_element_def
packageable_element_def  : type_def | subprogram_def
subprogram_def           : SUBPROGRAM IDENTIFIER LPAREN parameter_def parameter_list RPAREN COMMA returned_type
parameter_list           : <empty> | parameter_list SEMICOLON parameter_def
parameter_def            : IDENTIFIER COLON parameter_mode IDENTIFIER COLONEQ VALUE
                         | IDENTIFIER COLON parameter_mode IDENTIFIER
param_mode               : IN OUT | IN | OUT
type_def                 : class_def | enum_def
visibility               : PRIVATE | PROTECTED | PUBLIC
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
    'package_def : PACKAGE_START IDENTIFIER dependance_list packageable_element_list PACKAGE_STOP'
    p[0] = Package(p[2], p[3])

def p_dependance_list_1(p):
    'dependance_list : '
    p[0] = []

def p_dependance_list_2(p):
    'dependance_list : dependance_list dependance_def'
    p[1].append(p[2])
    p[0] = p[1]

def p_dependance_def(p):
    'dependance_def : with IDENTIFIER'
    p[0] = Dependance(p[2], p[3])

def p_packageable_element_list_1(p):
    'packageable_element_list : '
    p[0] = []

def p_packageable_element_list_2(p):
    'packageable_element_list : packageable_element_list packageable_element'
    p[1].append(p[2])
    p[0] = p[1]

def p_packageable_element(p):
    '''packageable_element : class_def
                           | subprogram_def'''
    p[0] = p[1]

def p_class_def(p):
    'class_def : CLASS_START IDENTIFIER CLASS_STOP'
    p[0] = Class(p[2])

def p_subprogram_def_1(p):
    'subprogram_def : PROCEDURE IDENTIFIER LPAREN parameter_def parameter_list RPAREN'
    p[5].append(p[4])
    p[0] = Procedure(p[2], p[5])

def p_subprogram_def_2(p):
    'subprogram_def : PROCEDURE IDENTIFIER'
    p[0] = Procedure(p[2], [])

def p_subprogram_def_3(p):
    'subprogram_def : FUNCTION IDENTIFIER LPAREN parameter_def parameter_list RPAREN COLON returned_type'
    name     = 2
    params   = 5
    returned = 8
    p[params].append(p[params - 1])
    p[0] = Function(p[name], p[returned], p[params])

def p_subprogram_def_4(p):
    'subprogram_def : FUNCTION IDENTIFIER COLON returned_type'
    name     = 2
    returned = 4
    p[0] = Function(p[name], p[returned], [])

def p_parameter_list_1(p):
    'parameter_list : '
    p[0] = []

def p_parameter_list_2(p):
    'parameter_list : parameter_list SEMICOLON parameter_def'
    p[1].append(p[3])
    p[0] = p[1]

def p_parameter_def(p):
    'parameter_def : IDENTIFIER COLON parameter_mode IDENTIFIER COLONEQ VALUE'
    p[0] = Parameter(p[1], p[3])

def p_parameter_def(p):
    'parameter_def : IDENTIFIER COLON parameter_mode IDENTIFIER'
    p[0] = Parameter(p[1], p[3])

def p_parameter_mode_1(p):
    'parameter_mode : IN OUT'
    p[0] = Parameter_Mode("in out")
    p[0] = p_mode_in_out

def p_parameter_mode_2(p):
    '''parameter_mode : IN
                      | OUT'''
    p[0] = Parameter_Mode(p[1])

def p_returned_type(p):
    'returned_type : IDENTIFIER'
    p[0] = p[1]

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
    data = open("data.txt", "r").read()

    result = parser.parse(data)
    if result != None:
        print(result)

if __name__ == '__main__':
    test_grammar()
