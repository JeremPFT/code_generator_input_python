import ply.lex as lex

reserved = {
    'abstract'         : 'ABSTRACT',
    'and'              : 'AND',
    'command'          : 'COMMAND',
    'end'              : 'END',
    'exceptions'       : 'EXCEPTIONS',
    'field'            : 'FIELD',
    'implementation'   : 'IMPLEMENTATION',
    'in'               : 'IN',
    'inout'            : 'INOUT',
    'is'               : 'IS',
    'limited'          : 'LIMITED',
    'operation'        : 'OPERATION',
    'or'               : 'OR',
    'out'              : 'OUT',
    'output_directory' : 'OUTPUT_DIRECTORY',
    'package'          : 'PACKAGE',
    'post'             : 'POST',
    'pre'              : 'PRE',
    'project'          : 'PROJECT',
    'query'            : 'QUERY',
    'readme_brief'     : 'README_BRIEF',
    'readme_title'     : 'README_TITLE',
    'return'           : 'RETURN',
    'subprogram'       : 'SUBPROGRAM',
    'type'             : 'TYPE',
    'use'              : 'USE',
    'value_object'     : 'VALUE_OBJECT',
    'vector'           : 'VECTOR',
    'with'             : 'WITH',
}

tokens = [
    'DOUBLEPERIOD', # ! before period
    'COLONEQ', # ! before colon, before equal
] + [
    'STAR',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'PERIOD',
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

def t_STAR(t):
    r'\*'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_DOUBLEPERIOD(t):
    r'\.\.'
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
    r'".*?"'
    return t

def t_INTEGER_VALUE(t):
    r'[0-9]+'
    return t

def t_VALUE(t):
    r'(".*")|([a-z0-9]+)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_eof(t):
    t.lexer.lineno = 1
    return None

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    print("line_start = {!s}, lexpos = {!s}".format(line_start, token.lexpos))
    return (token.lexpos - line_start) + 1

lexer = lex.lex(debug = False)
lexer.lineno = 1

# def build_lexer():
#     return lex.lex(debug = False)

def test_lexer(data):
    lexer.input(data)

    token = lexer.token()
    while token != None :
        print(token)
        print('column: ' + str(find_column(data, token)))
        token = lexer.token()

if __name__ == '__main__':
    test_lexer()
