#! python3

import os
import ply.yacc as yacc

from src.lexer import tokens

from src.uml_model import *

from src.utils import dbg

'''
(fset 'copy-grammar-rule
[?\C-s ?: ?\C-j ?  ?\' ?\' ?\' return ?\M-f ?\M-b ?\C-  ?\C-s ?\' ?\' ?\' ?\C-a ?\M-w ?\C-x ?o ?\C-y ?\C-x ?o])
'''

'''
project_item                       : project_init project_content project_close
project_init                       : PROJECT IDENTIFIER
project_content                    : output_directory project_type package_list
project_close                      : END PROJECT IDENTIFIER SEMICOLON
project_close                      : END PROJECT SEMICOLON
package_list                       :
package_list                       : package_list package
package                            : package_init package_content package_close
package_init                       : PACKAGE IDENTIFIER
package_content                    : dependance_list packageable_element_list
package_close                      : END PACKAGE IDENTIFIER SEMICOLON
package_close                      : END PACKAGE SEMICOLON
dependance_list                    :
dependance_list                    : dependance_list dependance
dependance                         : WITH IDENTIFIER
dependance                         : USE IDENTIFIER
dependance                         : LIMITED WITH IDENTIFIER
packageable_element_list           :
packageable_element_list           : packageable_element_list packageable_element
packageable_element                : operation
                                   | type_item
type_item                          : exception_block                 // TODO
                                   | value_object
value_object                       : value_object_init value_object_content value_object_close
value_object_init                  : value_object_init_abstract_inherit
                                   | value_object_init_abstract
                                   | value_object_init_inherit
                                   | value_object_init_simple
value_object_init_abstract_inherit : ABSTRACT VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN
value_object_init_abstract         : ABSTRACT VALUE_OBJECT IDENTIFIER
value_object_init_inherit          : VALUE_OBJECT IDENTIFIER LPAREN IDENTIFIER RPAREN
value_object_init_simple           : VALUE_OBJECT IDENTIFIER
value_object_content               : dependance_list feature_list
value_object_close                 : END VALUE_OBJECT IDENTIFIER SEMICOLON
value_object_close                 : END VALUE_OBJECT SEMICOLON
feature_list                       :
feature_list                       : feature_list feature
feature                            : property SEMICOLON
                                   | operation SEMICOLON
operation                          : operation_init parameter_list operation_return
operation_init                     : OPERATION IDENTIFIER
operation_return                   :
operation_return                   : RETURN IDENTIFIER
parameter_list                     :
parameter_list                     : LPAREN parameter_item RPAREN
parameter_list                     : LPAREN parameter_item_list parameter_item RPAREN
parameter_item_list                : parameter_item SEMICOLON
parameter_item_list                : parameter_item_list parameter_item
parameter_item                     : IDENTIFIER COLON direction IDENTIFIER
direction                          : INOUT
                                   | OUT
                                   | IN
property                           : IDENTIFIER COLON IDENTIFIER
project_type                       : TYPE IDENTIFIER SEMICOLON
output_directory                   : OUTPUT_DIRECTORY string
string                             : string AMP STRING_VALUE
string                             : STRING_VALUE
'''

def check_closing_name(p, class_name):
    if p[3] != p[-2].name:
        print("WARNING closed %s %s is not opened %s %s" % \
              (class_name, p[3], class_name, p[-2].name))

#
# - project
#

def p_project_item_no_named(p):
    '''
    project : PROJECT OUTPUT_DIRECTORY
    '''
    raise NoNameError("SyntaxError line {!s}: project need a name".format(p.lineno(1)))

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

# def p_project_init_no_name(p):
#     '''
#     project_init : PROJECT
#     '''
#     # p.parser.error = NoNameError()
#     # print("SyntaxError line {!s}: project need a name".format(p.lineno(1)))
#     # p[0] = Project(name = "")
#     p.parser.error = NoNameError("SyntaxError line {!s}: project need a name".format(p.lineno(1)))
#     p_error(p)

def p_project_content(p):
    '''
    project_content : output_directory project_type readme_content package_list
    '''
    p[-1].set_output_directory(p[1])
    p[-1].set_type(p[2])

    for package_item in p[3]:
        p[-1].add_package(package_item)

def p_readme_content(p):
    '''
    reamde_content : REAMDE_TITLE string REAMDE_BRIEF string
    '''
    p[-2].set_readme_title(p[2])
    p[-2].set_readme_brief(p[4])

def p_project_close_with_name(p):
    '''
    project_close : END PROJECT IDENTIFIER SEMICOLON
    '''
    check_closing_name(p, "project")

def p_project_close(p):
    '''
    project_close : END PROJECT SEMICOLON
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
    p[-1].packageable_element_list = p[2]

def p_package_close_with_name(p):
    '''
    package_close : END PACKAGE IDENTIFIER SEMICOLON
    '''
    check_closing_name(p, "package")

def p_package_close(p):
    '''
    package_close : END PACKAGE SEMICOLON
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
    '''
    packageable_element : operation
                        | type_item
    '''
    p[0] = p[1]

    p.parser.current_package.add_owned_member(p[0])

def p_type_item(p):
    '''
    type_item : value_object
              | exception_block
    '''
    p[0] = p[1]

def p_exception_block(p):
    '''
    exception_block : EXCEPTIONS exception_list exception_item END EXCEPTIONS SEMICOLON
    '''

def p_exception_list_empty(p):
    '''
    exception_list :
    '''
    p[0] = []

def p_exception_list_more(p):
    '''
    exception_list : exception_list exception_item
    '''
    p[1].append(p[2])
    p[0] = [1]

def p_exception_item(p):
    '''
    exception_item : IDENTIFIER
    '''
    p[0] = p[1]

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

def p_value_object_close_with_name(p):
    '''
    value_object_close : END VALUE_OBJECT IDENTIFIER SEMICOLON
    '''
    check_closing_name(p, "value_object")

def p_value_object_close(p):
    '''
    value_object_close : END VALUE_OBJECT SEMICOLON
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

# pseudocode def p_implementation_from_file(p):
# pseudocode     '''
# pseudocode     implementation : IMPLEMENTATION string SEMICOLON
# pseudocode     '''
# pseudocode
# pseudocode     implementation_file = open(p[2])
# pseudocode
# pseudocode     # TODO following is pseudo code
# pseudocode
# pseudocode     declaration = substring(path = implementation_file,
# pseudocode                             from = position_of ("[^a-z_]is[^a-z_]"),
# pseudocode                             end  = position_of ("[^a-z_]begin[^a-z_]"))
# pseudocode
# pseudocode     body = substring(path = implementation_file,
# pseudocode                      from = position_of ("[^a-z_]begin[^a-z_]"),
# pseudocode                      end  = last_position_of ("[^a-z_]end[^a-z_]"))
# pseudocode
# pseudocode def p_implementation(p):
# pseudocode     '''
# pseudocode     implementation : declaration_item body_item
# pseudocode     '''
# pseudocode     pass
# pseudocode
# pseudocode def p_declaration(p):
# pseudocode     '''
# pseudocode     declaration_item : DECLARATION declaration_content
# pseudocode     '''

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

def p_project_type(p):
    '''
    project_type : TYPE IDENTIFIER SEMICOLON
    '''
    prj_type = p[2]

    if not prj_type in Project.TYPES:
        print("!! SyntaxError: project type {!r} undefined line {}".format(prj_type, p.lineno(1)))
        raise SyntaxError

    p[0] = p[2]

def p_output_directory(p):
    '''
    output_directory : OUTPUT_DIRECTORY string SEMICOLON
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
        print("!! SyntaxError: end of file")
        return

    if p.parser.error != None:
        print(str(p.parser.error))

        tok = None
        while True:
            tok = parser.token()
            if tok == None:
                break
            else:
                print("ignoring token line {!s}".format(tok.lineno))
    else:
        print("!! SyntaxError in input")
        message = "line %s: unexpected %s %s" % (str(p.lineno), str(p.type), str(p))
        print(message)

parser = yacc.yacc(debug = False)
parser.error = None
parser.current_project   = None
parser.current_package   = None
parser.current_class     = None
parser.current_procedure = None

def test_grammar(data):
    result = parser.parse(data, debug = False)
    print("return object " + str(type(result)))
    return result

if __name__ == '__main__':
    prj = test_grammar()
    if prj != None:
        print(os.linesep + ("=" * 60) + os.linesep)
        print(prj)
        print(os.linesep + "=" * 60)
