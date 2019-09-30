import ply.lex as lex

reserved = {
    'project'          : 'PROJECT_START',
    'end_project'      : 'PROJECT_STOP',
    'output_directory' : 'OUTPUT_DIRECTORY',
    'package'          : 'PACKAGE_START',
    'end_package'      : 'PACKAGE_STOP',
    'class'            : 'CLASS_START',
    'end_class'        : 'CLASS_STOP',
    'field'            : 'FIELD_START',
    'end_field'        : 'FIELD_STOP',
    'use'              : 'USE',
    'subprogram'       : 'SUBPROGRAM',
}

tokens = [
    'IDENTIFIER',
    'COMMENT',
    'STRING',
] + list(reserved.values())

t_ignore  = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_COMMENT(t):
    r'-- .*'
    pass

def t_STRING(t):
    r'".*"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_eof(t):
    return None

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex(debug = 0)

def test_lexer():
    data = '''
project project_name
output_directory "c:\"
-- a basic example to test the parser
end_project
    '''

    lexer.input(data)

    token = lexer.token()
    while token != None :
        print(token)
        print('column: ' + str(find_column(data, token)))
        token = lexer.token()

if __name__ == '__main__':
    test_lexer()
