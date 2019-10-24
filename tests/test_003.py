import unittest

from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parse_input
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
        print(__class__)
        filename = "~/workspace/code_generator_py/tests/test_003/test_003.dsl"
        cls.project = parse_input(filename)

        template_dir = directory("~/workspace/code_generator_py/tests/test_003")
        template_engine = Template_Engine(template_directory = template_dir)
        generator = Generator_Ada_Project(template_engine)
        generator.output(cls.project)

    @classmethod
    def tearDownClass(cls):
        rmdir("~/tests")

    def test_field_name(self):
        print(__name__)
        self.assertEqual(Test_Project_Nominal.project.name,
                         "test_003",
                         "project name")

    def test_field_output_directory(self):
        self.assertEqual(Test_Project_Nominal.project._output_directory,
                         directory("~/tests/test_003"),
                         "output directory")

    def test_field_title(self):
        self.assertEqual(Test_Project_Nominal.project._title,
                         "test 003 title",
                         "project title")

    def test_field_brief(self):
        self.assertEqual(Test_Project_Nominal.project._brief,
                         "test 003 brief",
                         "project brief")

    def _setdown(self):
        super()._setdown()

    def _build_test_list(self):
        for test in (
                check_project,
                check_prj_dir,
                check_src_dir,
                check_gpr_file,
        ):
            self._add_test(test)

    def get_project(self):
        return self.__project
