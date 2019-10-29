#!python3.8

import unittest

# from src.dsl_grammar import test_grammar
# from src.lexer import test_lexer
# from src.output_ada import Output_Ada
# import src.template_engine

# data = '''
# project project_name
# output_directory "c:\"
# -- a basic example to test the parser
# end_project
#     '''

# data = open("input.dsl", "r").read()
# prj = test_grammar(data)
# # if prj != None:
# #     print(os.linesep + ("=" * 60) + os.linesep)
# #     print(prj)
# #     print(os.linesep + "=" * 60)
# generator = Output_Ada()
# generator.output(prj)

# src.template_engine.test_engine()


from test_001 import Test_Project_Nominal_001
from test_002 import Test_Unnamed_Project
from test_003 import Test_Project_Nominal_003

unittest.main()
