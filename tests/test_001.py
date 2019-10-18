import unittest

from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parser
from src.template_engine import Template_Engine

from src.utils import (
    directory,
    rmdir,
    dir_exists,
    text_files_match,
)


class Test_Project_Nominal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_file_name = directory("~/workspace/code_generator_py/tests/" +
                                         "test_001/test_001.dsl")
        cls.input_file = open(cls.input_file_name, "r")
        cls.project = parser.parse(cls.input_file.read(), debug = False)

        # cls.project = parse_input("~/workspace/code_generator_py/tests/" +
        #                           "test_001/test_001.dsl")

        print(str(cls.project))

        template_dir = directory("~/workspace/code_generator_py/tests/test_001")
        template_engine = Template_Engine(template_directory = template_dir)
        generator = Generator_Ada_Project(template_engine)
        generator.output(cls.project)

    @classmethod
    def tearDownClass(cls):
        cls.input_file.close()
        rmdir("~/tests")

    def test_field_name(self):
        self.assertEqual(Test_Project_Nominal.project.name,
                         "test_001",
                         "project name")

    def test_field_output_directory(self):
        self.assertEqual(Test_Project_Nominal.project._output_directory,
                         directory("~/tests/test_001"),
                         "output directory")

    def test_field_title(self):
        self.assertEqual(Test_Project_Nominal.project._title,
                         "test 001 title",
                         "bad project title")

    def test_field_brief(self):
        self.assertEqual(Test_Project_Nominal.project._brief,
                         "test 001 brief",
                         "project brief")
