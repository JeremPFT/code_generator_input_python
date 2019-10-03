#! python3

import os
import ply.yacc as yacc

import project_parser_lexer
from project_parser_lexer import tokens

from model import Project, \
    Package, \
    Class, \
    Operation, \
    Parameter, \
    Dependance, \
    Field

'''
project                  : PROJECT IDENTIFIER output_directory package_list END PROJECT
output_directory         : string
string                   : STRING_VALUE | string AMP STRING_VALUE
package_list             : <empty> | package_list package_item
package_item              : PACKAGE IDENTIFIER dependance_list packageable_element_list END PACKAGE
dependance_list          : <empty> | dependance_list dependance_item
dependance_item           : WITH IDENTIFIER
packageable_element_list : <empty> | packageable_element_list packageable_element_item
packageable_element_item  : type_item | subprogram_item
subprogram_item           : SUBPROGRAM IDENTIFIER LPAREN parameter_item parameter_list RPAREN COMMA returned_type
parameter_list           : <empty> | parameter_list SEMICOLON parameter_item
parameter_item            : IDENTIFIER COLON parameter_mode IDENTIFIER COLONEQ VALUE
                         | IDENTIFIER COLON parameter_mode IDENTIFIER
param_mode               : IN OUT | IN | OUT
type_item                 : class_item | enum_item
visibility               : PRIVATE | PROTECTED | PUBLIC
'''

def p_project(p):
    'project : PROJECT IDENTIFIER output_directory package_list END PROJECT'
    p[0] = \
    Project(name             = p[2],
            output_directory = p[3],
            package_list     = p[4])

def p_output_directory(p):
    'output_directory : OUTPUT_DIRECTORY string'
    p[0] = p[2]

def p_string_more_than_one(p):
    'string : string AMP STRING_VALUE'
    left = p[1].replace('"', '')
    right = p[3].replace('"', '')
    p[0] = '"' + left + right + '"'

def p_string_one(p):
    'string : STRING_VALUE'
    p[0] = p[1]

def p_package_list_empty(p):
    'package_list : '
    p[0] = []

def p_package_list_more(p):
    'package_list : package_list package_item'
    p[1].append(p[2])
    p[0] = p[1]

def p_package_item(p):
    'package_item : PACKAGE IDENTIFIER build_package dependance_list packageable_element_list END PACKAGE IDENTIFIER'
    print("=" * 10 + " package_item rule")
    p[3].dependance_list = p[4]
    p[3].packageable_element_list = p[5]
    p[0] = p[3]
    p.parser.current_package = p[0]

def p_build_package(p):
    'build_package :'
    print("=" * 10 + " build_package rule")
    p[0] = Package(name = p[-1])

def p_dependance_list_empty(p):
    'dependance_list : '
    p[0] = []

def p_dependance_list_more(p):
    'dependance_list : dependance_list dependance_item'
    p[1].append(p[2])
    p[0] = p[1]

def p_dependance_item_with(p):
    'dependance_item : WITH IDENTIFIER'
    p[0] = Dependance(mode = p[1], imported_unit = p[2])

def p_dependance_item_use(p):
    'dependance_item : USE IDENTIFIER'
    p[0] = Dependance(mode = p[1], imported_unit = p[2])

def p_dependance_item_limited_with(p):
    'dependance_item : LIMITED WITH IDENTIFIER'
    p[0] = Dependance(mode = p[1] + p[2], imported_unit = p[3])

def p_packageable_element_list_empty(p):
    'packageable_element_list : '
    p[0] = []

def p_packageable_element_list_more(p):
    'packageable_element_list : packageable_element_list packageable_element_item'
    p[1].append(p[2])
    p[0] = p[1]

def p_packageable_element_item(p):
    '''packageable_element_item : subprogram_item
                                | value_object_item
    '''
    p[0] = p[1]

def p_value_object_item(p):
    'value_object_item : value_object_begin value_object_content value_object_end'
    p[0] = p[1]
    print("new Class: " + str(p[0]))

def p_value_object_begin_abstract_inherit(p):
    'value_object_begin : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'
    is_abstract = True
    parent_name = p[5]
    for element in p.parser.current_package.packageable_element_list:
        if element.name == parent_name:
            parent = element


    name = p[3]
    p[0] = Class(name = name, is_abstract = is_abstract, parent = parent)

def p_value_object_begin_abstract(p):
    'value_object_begin : ABSTRACT VALUE_OBJECT IDENTIFIER'
    is_abstract = True
    name = p[3]
    p[0] = Class(name = name, is_abstract = is_abstract)

# def p_value_object_begin_inherit(p):
#     'value_object_begin : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'

# def p_value_object_begin_simple(p):
#     'value_object_begin : VALUE_OBJECT IDENTIFIER'

def p_value_object_content(p):
    'value_object_content : dependance_list feature_list'
#     'value_object_content : dependance_list initialization behavior_list'
    p[-1].dependance_list = p[1]

def p_value_object_end(p):
    'value_object_end : END VALUE_OBJECT IDENTIFIER'
    name = p[3]
    if name != p[-2].name:
        print("WARNING closing name '%s' doesn't match opening name '%s'" % (p[3], p[-2].name))

def p_feature_list_none(p):
    'feature_list :'
    p[0] = []

def p_feature_list_more(p):
    'feature_list : feature_list feature_item'
    print("READ FEATURE: " + str(p[2]))
    print("IN " + str(p[-2].name))
    if p[2].__class__.__name__ == "Field":
        p[-2].field_list.append(p[2])

def p_feature_item(p):
    '''feature_item : field_item
                    | operation_item'''
    p[0] = p[1]

def p_operation_item(p):
    'operation_item : INITIALIZE'
    print("read operation")

def p_field_item(p):
    'field_item : IDENTIFIER COLON IDENTIFIER'
    print("read field %s : %s" % (p[1], p[3]))
    p[0] = Field(name = p[1], of_type = p[3])

# def p_initialization_none(p):
#     'initialization :'

# def p_initialization_item(p):
#     'initialization : INITIALIZE'
#     # 'initialization : INITIALIZE signature implementation'
#     p[-1].append(Procedure(name="initialize"))

# def p_signature(p):
#     'signature : parameter_list'

# def p_behavior_list_empty(p):
#     'behavior_list : '
#     p[0] = []

# def p_behavior_list_more(p):
#     'behavior_list : behavior_list behavior_item'
#     p[0] = []

# def p_behavior_item(p):
#     'behavior_item : behavior_begin behavior_content behavior_end'
#     p[0] = Class(p[2])

# def p_behavior_begin_init(p):
#     'behavior_begin : INITIALIZE contract'

# def p_behavior_begin_query(p):
#     'behavior_begin : QUERY IDENTIFIER RETURN IDENTIFIER contract'

# def p_behavior_begin_command(p):
#     'behavior_begin : COMMAND IDENTIFIER contract'

# def p_contract_empty(p):
#     'contract : '
#     p[0] = []

# def p_contract_more(p):
#     'contract : contract contract_item'
#     p[0] = []

# def p_contract_item(p):
#     '''contract_item : PRE condition_list
#                      | POST condition_list
#     '''
#     if p[1] == "pre":
#         p[0] = Pre_Condition(condition_list)
#     elif p[1] == "post":
#         p[0] = Post_Condition(condition_list)

def p_subprogram_item_with_params(p):
    'subprogram_item : PROCEDURE IDENTIFIER LPAREN parameter_item parameter_list RPAREN'
    p[5].append(p[4])
    p[0] = Procedure(p[2], p[5])

def p_subprogram_item_no_param(p):
    'subprogram_item : PROCEDURE IDENTIFIER'
    p[0] = Procedure(p[2], [])

def p_subprogram_item_3(p):
    'subprogram_item : FUNCTION IDENTIFIER LPAREN parameter_item parameter_list RPAREN COLON returned_type'
    name     = 2
    params   = 5
    returned = 8
    p[params].append(p[params - 1])
    p[0] = Function(p[name], p[returned], p[params])

def p_subprogram_item_4(p):
    'subprogram_item : FUNCTION IDENTIFIER COLON returned_type'
    name     = 2
    returned = 4
    p[0] = Function(p[name], p[returned], [])

def p_parameter_list_empty(p):
    'parameter_list :'
    p[0] = []

def p_parameter_list_one_or_more(p):
    'parameter_list : parameter_item'
    p[0] = []

def p_parameter_list_more(p):
    'parameter_list : LPAREN parameter_list SEMICOLON parameter_item RPAREN'
    p[1].append(p[3])
    p[0] = p[1]

def p_parameter_item_1(p):
    'parameter_item : IDENTIFIER COLON parameter_mode IDENTIFIER COLONEQ VALUE'
    p[0] = Parameter(p[1], p[3])

def p_parameter_item_2(p):
    'parameter_item : IDENTIFIER COLON parameter_mode IDENTIFIER'
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
    message += " " + str(p)
    print(message)

parser = yacc.yacc()
parser.current_package = None

def test_grammar():
    data = open("input.dsl", "r").read()

    result = parser.parse(data)
    if result != None:
        print(os.linesep + ("=" * 60) + os.linesep)
        print(result)
        print("=" * 60)

if __name__ == '__main__':
    test_grammar()
