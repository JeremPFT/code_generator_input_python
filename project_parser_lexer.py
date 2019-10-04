import ply.lex as lex

reserved = {
    'abstract'         : 'ABSTRACT',
    'and'              : 'AND',
    'or'               : 'OR',
    'command'          : 'COMMAND',
    'end'              : 'END',
    'field'            : 'FIELD',
    'function'         : 'FUNCTION',
    'implementation'   : 'IMPLEMENTATION',
    'in'               : 'IN',
    'initialize'       : 'INITIALIZE',
    'is'               : 'IS',
    'limited'          : 'LIMITED',
    'out'              : 'OUT',
    'output_directory' : 'OUTPUT_DIRECTORY',
    'package'          : 'PACKAGE',
    'post'             : 'POST',
    'pre'              : 'PRE',
    'procedure'        : 'PROCEDURE',
    'project'          : 'PROJECT',
    'query'            : 'QUERY',
    'return'           : 'RETURN',
    'subprogram'       : 'SUBPROGRAM',
    'use'              : 'USE',
    'value_object'     : 'VALUE_OBJECT',
    'vector'           : 'VECTOR',
    'with'             : 'WITH',
}

tokens = [
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COLONEQ',
    'COLON',
    'AMP',
    'IDENTIFIER',
    'COMMENT',
    'STRING_VALUE',
    'INTEGER_VALUE',
    'SUPERIOR',
    'INFERIOR',
    'EQUAL',
    'VALUE',
] + list(reserved.values())

t_ignore  = ' \t'

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_COLON(t):
    r':'
    return t

def t_COLONEQ(t):
    r':='
    return t

def t_AMP(t):
    r'&'
    return t

def t_SUPERIOR(t):
    r'>'
    return t

def t_INFERIOR(t):
    r'<'
    return t

def t_EQUAL(t):
    r'='
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9.]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_COMMENT(t):
    r'--.*'
    pass

def t_STRING_VALUE(t):
    r'".*"'
    return t

def t_INTEGER_VALUE(t):
    r'[0-9]*'
    return t

def t_VALUE(t):
    r'(".*")|([a-z0-9]+)'

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
