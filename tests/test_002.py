import unittest

import os

from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parser
from src.template_engine import Template_Engine
from src.uml_model import NoNameError

from src.utils import (
    directory,
    rmdir,
    dir_exists,
    text_files_match,
)


class Test_Unnamed_Project(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_data = open("tests/test_002/test_002.dsl", "r").read()

    # @classmethod
    # def tearDownClass(cls):
#        cls.input_data.close()

    def test_no_name_project(self):
        self.assertRaises(NoNameError,
                          parser.parse,
                          (Test_Unnamed_Project.input_data))
