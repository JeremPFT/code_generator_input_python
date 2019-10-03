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

def check_closing_name(p, class_name):
    if p[3] != p[-2].name:
        print("WARNING closed %s %s is not opened %s %s" % \
              (class_name, p[3], class_name, p[-2].name))


#
# - project
#


def p_project_instance(p):
    'project : project_init project_content project_close'

    p[0] = p[1]


def p_project_init(p):
    'project_init : PROJECT IDENTIFIER'

    p[0] = Project(name = p[2])


def p_project_content(p):
    'project_content : output_directory package_list'

    p[-1].output_directory = p[1]
    p[-1].package_list     = p[2]


def p_project_close_named(p):
    'project_close : END PROJECT IDENTIFIER'

    check_closing_name(p, "project")


def p_project_close(p):
    'project_close : END PROJECT'

    pass


#
# - package
#


def p_package_list_empty(p):
    'package_list : '

    p[0] = []


def p_package_list_more(p):
    'package_list : package_list package'

    p[1].append(p[2])
    p[0] = p[1]


def p_package_instance(p):
    'package : package_init package_content package_close'

    p[0]                     = p[1]
    p.parser.current_package = p[0]


def p_package_init(p):
    'package_init : PACKAGE IDENTIFIER'

    p[0] = Package(name = p[2])


def p_package_content(p):
    'package_content : dependance_list packageable_element_list'

    p[-1].dependance_list          = p[1]
    p[-1].packageable_element_list = p[2]


def p_package_close_named(p):
    'package_close : END PACKAGE IDENTIFIER'

    check_closing_name(p, "package")


def p_package_close(p):
    'package_close : END PACKAGE'

    pass


#
# - dependancy
#


def p_dependance_list_empty(p):
    'dependance_list : '

    p[0] = []


def p_dependance_list_more(p):
    'dependance_list : dependance_list dependance'

    p[1].append(p[2])
    p[0] = p[1]


def p_dependance_with(p):
    'dependance : WITH IDENTIFIER'

    p[0] = Dependance(mode = p[1], imported_unit = p[2])


def p_dependance_use(p):
    'dependance : USE IDENTIFIER'

    p[0] = Dependance(mode = p[1], imported_unit = p[2])


def p_dependance_limited_with(p):
    'dependance : LIMITED WITH IDENTIFIER'

    p[0] = Dependance(mode = p[1] + p[2], imported_unit = p[3])


#
# - packageable_element
#


def p_packageable_element_list_empty(p):
    'packageable_element_list : '

    p[0] = []


def p_packageable_element_list_more(p):
    'packageable_element_list : packageable_element_list packageable_element'

    p[1].append(p[2])
    p[0] = p[1]


def p_packageable_element(p):
    '''packageable_element : subprogram
                                | value_object
    '''

    p[0] = p[1]


#
# - value_object
#


def p_value_object(p):
    'value_object : value_object_init value_object_content value_object_close'

    p[0] = p[1]


def p_value_object_init_abstract_inherit(p):
    'value_object_init : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'

    is_abstract = True
    parent_name = p[5]

    name = p[3]
    p[0] = Class(name = name, is_abstract = is_abstract, parent = parent_name)


def p_value_object_init_abstract(p):
    'value_object_init : ABSTRACT VALUE_OBJECT IDENTIFIER'

    is_abstract = True
    name = p[3]
    p[0] = Class(name = name, is_abstract = is_abstract)

# def p_value_object_init_inherit(p):
#     'value_object_init : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN'

# def p_value_object_init_simple(p):
#     'value_object_init : VALUE_OBJECT IDENTIFIER'


def p_value_object_content(p):
    'value_object_content : dependance_list feature_list'

    p[-1].dependance_list = p[1]
    p[1] = None


def p_value_object_close_named(p):
    'value_object_close : END VALUE_OBJECT IDENTIFIER'

    check_closing_name(p, "value_object")


def p_value_object_close(p):
    'value_object_close : END VALUE_OBJECT'

    pass


#
# - feature
#


def p_feature_list_none(p):
    'feature_list :'

    p[0] = []


def p_feature_list_more(p):
    'feature_list : feature_list feature'

    if p[2].__class__.__name__ == "Field":
        p[-2].field_list.append(p[2])


def p_feature(p):
    '''feature : field
                    | operation'''

    p[0] = p[1]


#
# - operation
#


def p_operation(p):
    'operation : INITIALIZE'

    pass


#
# - field
#


def p_field(p):
    'field : IDENTIFIER COLON IDENTIFIER'

    p[0] = Field(name = p[1], of_type = p[3])

# def p_initialization_none(p):
#     'initialization :'

# def p_initialization(p):
#     'initialization : INITIALIZE'
#     # 'initialization : INITIALIZE signature implementation'
#     p[-1].append(Procedure(name="initialize"))

# def p_signature(p):
#     'signature : parameter_list'

# def p_behavior_list_empty(p):
#     'behavior_list : '
#     p[0] = []

# def p_behavior_list_more(p):
#     'behavior_list : behavior_list behavior'
#     p[0] = []

# def p_behavior(p):
#     'behavior : behavior_init behavior_content behavior_end'
#     p[0] = Class(p[2])

# def p_behavior_init_init(p):
#     'behavior_init : INITIALIZE contract'

# def p_behavior_init_query(p):
#     'behavior_init : QUERY IDENTIFIER RETURN IDENTIFIER contract'

# def p_behavior_init_command(p):
#     'behavior_init : COMMAND IDENTIFIER contract'

# def p_contract_empty(p):
#     'contract : '
#     p[0] = []

# def p_contract_more(p):
#     'contract : contract contract'
#     p[0] = []

# def p_contract(p):
#     '''contract : PRE condition_list
#                      | POST condition_list
#     '''
#     if p[1] == "pre":
#         p[0] = Pre_Condition(condition_list)
#     elif p[1] == "post":
#         p[0] = Post_Condition(condition_list)


def p_subprogram_with_params(p):
    'subprogram : PROCEDURE IDENTIFIER LPAREN parameter parameter_list RPAREN'

    p[5].append(p[4])
    p[0] = Procedure(p[2], p[5])


def p_subprogram_no_param(p):
    'subprogram : PROCEDURE IDENTIFIER'

    p[0] = Procedure(p[2], [])


def p_subprogram_3(p):
    'subprogram : FUNCTION IDENTIFIER LPAREN parameter parameter_list RPAREN COLON returned_type'

    name     = 2
    params   = 5
    returned = 8
    p[params].append(p[params - 1])
    p[0] = Function(p[name], p[returned], p[params])


def p_subprogram_4(p):
    'subprogram : FUNCTION IDENTIFIER COLON returned_type'

    name     = 2
    returned = 4
    p[0] = Function(p[name], p[returned], [])


def p_parameter_list_empty(p):
    'parameter_list :'

    p[0] = []


def p_parameter_list_one(p):
    'parameter_list : parameter'

    p[0] = []


def p_parameter_list_more(p):
    'parameter_list : LPAREN parameter_list SEMICOLON parameter RPAREN'

    p[1].append(p[3])
    p[0] = p[1]


def p_parameter_init(p):
    'parameter : IDENTIFIER COLON parameter_mode IDENTIFIER COLONEQ VALUE'

    p[0] = Parameter(p[1], p[3])


def p_parameter(p):
    'parameter : IDENTIFIER COLON parameter_mode IDENTIFIER'

    p[0] = Parameter(p[1], p[3])


def p_parameter_mode_inout(p):
    'parameter_mode : IN OUT'

    p[0] = Parameter_Mode("in out")
    p[0] = p_mode_in_out


def p_parameter_mode_in_or_out(p):
    '''parameter_mode : IN
                      | OUT'''

    p[0] = Parameter_Mode(p[1])


def p_returned_type(p):
    'returned_type : IDENTIFIER'

    p[0] = p[1]


def p_output_directory(p):
    'output_directory : OUTPUT_DIRECTORY string'

    p[0] = p[2]


def p_string_one_or_more(p):
    'string : string AMP STRING_VALUE'

    left  = p[1].replace('"', '')
    right = p[3].replace('"', '')
    p[0]  = '"' + left + right + '"'


def p_string_one(p):
    'string : STRING_VALUE'

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

parser = yacc.yacc(debug = True)
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
