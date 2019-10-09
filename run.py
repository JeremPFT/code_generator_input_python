from src.project_parser_dsl_grammar import test_grammar
from src.project_parser_lexer import test_lexer

data = '''
project project_name
output_directory "c:\"
-- a basic example to test the parser
end_project
    '''

data = open("input.dsl", "r").read()
test_grammar(data)
