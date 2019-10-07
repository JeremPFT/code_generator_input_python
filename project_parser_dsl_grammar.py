#! python3

import os
import ply.yacc as yacc

import project_parser_lexer
from project_parser_lexer import tokens

from model import (
    Class,
    Dependance,
    Property,
    Operation,
    Package,
    Parameter,
    Project,
)

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

def p_project_item(p):
    '''
    project : project_init project_content project_close
    '''
    p[0] = p[1]

def p_project_init(p):
    '''
    project_init : PROJECT IDENTIFIER
    '''
    p[0] = Project(name = p[2])
    p.parser.current_project = p[0]

def p_project_content(p):
    '''
    project_content : output_directory package_list
    '''
    p[-1].set_output_directory(p[1])
    for package_item in p[2]:
        p[-1].add_package(package_item)
    # p[-1].output_directory = p[1]
    # p[-1].package_list     = p[2]

def p_project_close_named(p):
    '''
    project_close : END PROJECT IDENTIFIER
    '''
    check_closing_name(p, "project")

def p_project_close(p):
    '''
    project_close : END PROJECT
    '''
    pass

#
# - package
#

def p_package_list_empty(p):
    '''
    package_list :
    '''
    p[0] = []

def p_package_list_more(p):
    '''
    package_list : package_list package
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_package_item(p):
    '''
    package : package_init package_content package_close
    '''
    p[0]                     = p[1]
    p.parser.current_package = p[0]

def p_package_init(p):
    '''
    package_init : PACKAGE IDENTIFIER
    '''
    p[0] = Package(name = p[2])
    p.parser.current_package = p[0]

def p_package_content(p):
    '''
    package_content : dependance_list packageable_element_list
    '''
    p[-1].dependance_list          = p[1]
    # p[-1].packageable_element_list = p[2]

def p_package_close_named(p):
    '''
    package_close : END PACKAGE IDENTIFIER
    '''
    check_closing_name(p, "package")

def p_package_close(p):
    '''
    package_close : END PACKAGE
    '''
    pass

#
# - dependancy
#

def p_dependance_list_empty(p):
    '''
    dependance_list :
    '''
    p[0] = []

def p_dependance_list_more(p):
    '''
    dependance_list : dependance_list dependance
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_dependance_with(p):
    '''
    dependance : WITH IDENTIFIER
    '''
    p[0] = Dependance(mode = p[1], imported_unit = p[2])

def p_dependance_use(p):
    '''
    dependance : USE IDENTIFIER
    '''
    p[0] = Dependance(mode = p[1], imported_unit = p[2])

def p_dependance_limited_with(p):
    '''
    dependance : LIMITED WITH IDENTIFIER
    '''
    p[0] = Dependance(mode = p[1] + p[2], imported_unit = p[3])

#
# - packageable_element
#

def p_packageable_element_list_empty(p):
    '''
    packageable_element_list :
    '''
    p[0] = []

def p_packageable_element_list_more(p):
    '''
    packageable_element_list : packageable_element_list packageable_element
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_packageable_element_item(p):
    '''packageable_element : operation
                           | value_object
    '''
    p[0] = p[1]

    p.parser.current_package.element_list.append(p[0])

#
# - value_object
#

def p_value_object_item(p):
    '''
    value_object : value_object_init value_object_content value_object_close
    '''
    p[0] = p[1]

def p_value_object_init(p):
    '''
    value_object_init : value_object_init_abstract_inherit
                      | value_object_init_abstract
                      | value_object_init_inherit
                      | value_object_init_simple
    '''
    p[0] = p[1]
    parser.current_class = p[0]

def p_value_object_init_abstract_inherit(p):
    '''
    value_object_init_abstract_inherit : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN
    '''
    is_abstract = True
    parent_name = p[5]
    name        = p[3]

    p[0] = Class(name        = name,
                 owner       = p.parser.current_package,
                 is_abstract = is_abstract,
                 parent_name = parent_name)

def p_value_object_init_abstract(p):
    '''
    value_object_init_abstract : ABSTRACT VALUE_OBJECT IDENTIFIER
    '''
    is_abstract = True
    name        = p[3]

    p[0] = Class(name        = name,
                 owner       = p.parser.current_package,
                 is_abstract = is_abstract)

def p_value_object_init_inherit(p):
    '''
    value_object_init_inherit : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN
    '''
    parent_name = p[4]
    name        = p[2]

    p[0] = Class(name        = name,
                 owner       = p.parser.current_package,
                 parent_name = parent_name)

def p_value_object_init_simple(p):
    '''
    value_object_init_simple : VALUE_OBJECT IDENTIFIER
    '''
    name = p[2]
    p[0] = Class(name  = name,
                 owner = p.parser.current_package)

def p_value_object_content(p):
    '''
    value_object_content : dependance_list feature_list
    '''
    p[-1].dependance_list = p[1]

    for feature in p[2]:
        if feature.__class__.__name__ == Property.__name__:
            p[-1].add_property(feature)
        elif feature.__class__.__name__ == Operation.__name__:
            p[-1].add_operation(feature)

def p_value_object_close_named(p):
    '''
    value_object_close : END VALUE_OBJECT IDENTIFIER
    '''
    check_closing_name(p, "value_object")

def p_value_object_close(p):
    '''
    value_object_close : END VALUE_OBJECT
    '''
    pass

#
# - feature
#

def p_feature_list_none(p):
    '''
    feature_list :
    '''
    p[0] = []

def p_feature_list_more(p):
    '''
    feature_list : feature_list feature
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_feature_item(p):
    '''
    feature : property SEMICOLON
            | operation SEMICOLON
    '''
    p[0] = p[1]

#
# - operation
#

def p_operation_item(p):
    '''
    operation : operation_init parameter_list operation_return
    '''
    operation     = p[1]
    parameters    = p[2]
    returned_type = p[3]

    for parameter in parameters:
        operation.add_parameter(parameter)

    if returned_type != None:
        operation.add_parameter(returned_type)

    p[0] = operation

def p_operation_init(p):
    '''
    operation_init : OPERATION IDENTIFIER
    '''
    p[0] = Operation(name = p[2])

def p_operation_return_none(p):
    '''
    operation_return :
    '''
    p[0] = None

def p_operation_return_one(p):
    '''
    operation_return : RETURN IDENTIFIER
    '''
    p[0] = Parameter(name      = "result",
                     of_type   = p[2],
                     direction = Parameter.DIRECTION_RETURN)

def p_parameter_list(p):
    '''
    parameter_list :
    '''
    p[0] = []

def p_parameter_list_one(p):
    '''
    parameter_list : LPAREN parameter_item RPAREN
    '''
    p[0] = [p[2]]

def p_parameter_list_more(p):
    '''
    parameter_list : LPAREN parameter_item_list parameter_item RPAREN
    '''
    p[0] = p[2]
    p[0].append(p[3])

def p_parameter_item_list_one(p):
    '''
    parameter_item_list : parameter_item SEMICOLON
    '''
    p[0] = [p[1]]

def p_parameter_item_list_more(p):
    '''
    parameter_item_list : parameter_item_list parameter_item
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_parameter_item(p):
    '''
    parameter_item : IDENTIFIER COLON direction IDENTIFIER
    '''
    p[0] = Parameter(name = p[1], direction = p[3], of_type = p[4])

def p_direction(p):
    '''
    direction : INOUT
              | OUT
              | IN
    '''
    p[0] = p[1]

#
# - implementation
#

def p_implementation_from_file(p):
    '''
    implementation : IMPLEMENTATION string SEMICOLON
    '''

    implementation_file = open(p[2])

    # TODO following is pseudo code

    declaration = substring(path = implementation_file,
                            from = position_of ("[^a-z_]is[^a-z_]"),
                            end  = position_of ("[^a-z_]begin[^a-z_]"))

    body = substring(path = implementation_file,
                     from = position_of ("[^a-z_]begin[^a-z_]"),
                     end  = last_position_of ("[^a-z_]end[^a-z_]"))

def p_implementation(p):
    '''
    implementation : declaration_item body_item
    '''
    pass

def p_declaration(p):
    '''
    declaration_item : DECLARATION declaration_content
    '''

#
# - property
#

def p_property_item(p):
    '''
    property : IDENTIFIER COLON IDENTIFIER
    '''
    p[0] = Property(name = p[1], of_type = p[3])

#
# - others
#

def p_output_directory(p):
    '''
    output_directory : OUTPUT_DIRECTORY string
    '''
    p[0] = p[2]

def p_string_one_or_more(p):
    '''
    string : string AMP STRING_VALUE
    '''
    left  = p[1].replace('"', '')
    right = p[3].replace('"', '')
    p[0]  = '"' + left + right + '"'

def p_string_one(p):
    '''
    string : STRING_VALUE
    '''
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

parser = yacc.yacc(debug = False)
parser.current_project   = None
parser.current_package   = None
parser.current_class     = None
parser.current_procedure = None

def test_grammar():
    data = open("input.dsl", "r").read()

    result = parser.parse(data, debug = False)
    if result != None:
        print(os.linesep + ("=" * 60) + os.linesep)
        print(result)
        print(os.linesep + "=" * 60)

if __name__ == '__main__':
    test_grammar()
