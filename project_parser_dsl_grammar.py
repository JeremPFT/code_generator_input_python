import ply.yacc as yacc

import project_parser_lexer
from project_parser_lexer import tokens

from model import Project, Package, Class, Subprogram, Procedure, Function, Parameter

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
    p[0] = Project(p[2], p[3], p[4])

def p_output_directory(p):
    'output_directory : OUTPUT_DIRECTORY string'
    p[0] = p[2]

def p_string_more_than_one(p):
    'string : string AMP STRING_VALUE'
    p[0] = p[1] + p[2]

def p_string_one(p):
    'string : STRING_VALUE'
    p[0] = p[1]

def p_package_list_empty(p):
    'package_list : '
    p[0] = []

def p_package_list_full(p):
    'package_list : package_list package_item'
    p[1].append(p[2])
    p[0] = p[1]

def p_package_item(p):
    'package_item : PACKAGE IDENTIFIER dependance_list packageable_element_list END PACKAGE'
    p[0] = Package(p[2], p[3])

def p_dependance_list_empty(p):
    'dependance_list : '
    p[0] = []

def p_dependance_list_full(p):
    'dependance_list : dependance_list dependance_item'
    p[1].append(p[2])
    p[0] = p[1]

def p_dependance_item_with(p):
    'dependance_item : WITH IDENTIFIER'
    p[0] = Dependance(p[2], p[3])

def p_dependance_item_use(p):
    'dependance_item : USE IDENTIFIER'
    p[0] = Dependance(p[2], p[3])

def p_dependance_item_limited_with(p):
    'dependance_item : LIMITED WITH IDENTIFIER'
    p[0] = Dependance(p[1] + p[2], p[3])

def p_packageable_element_list_empty(p):
    'packageable_element_list : '
    p[0] = []

def p_packageable_element_list_one_or_more(p):
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
    p[0] = Class(p[2])

def p_value_object_begin_abstract_params(p):
    'value_object_begin : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'
    is_abstract = true
    parent = 5
    name = 3
    the_class = Class(name = p[name], is_abstract = is_abstract, parent = p[parent])

def p_value_object_begin_abstract_no_param(p):
    'value_object_begin : ABSTRACT VALUE_OBJECT IDENTIFIER'

def p_value_object_begin_params(p):
    'value_object_begin : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'

def p_value_object_begin_no_param(p):
    'value_object_begin : VALUE_OBJECT IDENTIFIER'

def p_value_object_content(p):
    'value_object_content : dependance_list initialization behavior_list'

def p_value_object_end(p):
    'value_object_end : END VALUE_OBJECT'

def p_behavior_list_empty(p):
    'behavior_list : '
    p[0] = []

def p_behavior_list_one_or_more(p):
    'behavior_list : behavior_list behavior_item'
    p[0] = []

def p_behavior_item(p):
    'behavior_item : behavior_begin behavior_content behavior_end'
    p[0] = Class(p[2])

def p_behavior_begin_init(p):
    'behavior_begin : INITIALIZE contract_list'

def p_behavior_begin_query(p):
    'behavior_begin : QUERY IDENTIFIER RETURN IDENTIFIER contract_list'

def p_behavior_begin_command(p):
    'behavior_begin : COMMAND IDENTIFIER contract_list'

def p_contract_list_empty(p):
    'contract_list : '
    p[0] = []

def p_contract_list_one_or_more(p):
    'contract_list : contract_list contract_item'
    p[0] = []

def p_contract_item(p):
    '''contract_item : PRE condition_list
                     | POST condition_list
    '''
    if p[1] == "pre":
        p[0] = Pre_Condition(condition_list)
    elif p[1] == "post"
        p[0] = Post_Condition(condition_list)

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

def p_parameter_list_1(p):
    'parameter_list : parameter_item'
    p[0] = []

def p_parameter_list_2(p):
    'parameter_list : parameter_list SEMICOLON parameter_item'
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

def test_grammar():
    data = open("input.dsl", "r").read()

    result = parser.parse(data)
    if result != None:
        print(result)

if __name__ == '__main__':
    test_grammar()
