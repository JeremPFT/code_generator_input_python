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

class Test_Project_Nominal_001(unittest.TestCase):
    '''
    check project fields and directory creation
    '''

    TEST_ID = "001"
    PROJECT = None

    @classmethod
    def setUpClass(cls):
        # print(cls)
        filename = "~/workspace/code_generator_py/tests/test_{0}/test_{0}.dsl"
        filename = filename.format(cls.TEST_ID)
        cls.project = parse_input(filename)

        template_dir = "~/workspace/code_generator_py/tests/test_{}"
        template_dir = template_dir.format(cls.TEST_ID)
        template_dir = directory(template_dir)

        template_engine = Template_Engine(template_directory = template_dir)
        generator = Generator_Ada_Project(template_engine)
        generator.output(cls.project)

    @classmethod
    def tearDownClass(cls):
        rmdir("~/tests")
        pass

    def test_field_name(self):
        self.assertEqual(self.__class__.project.name,
                         "test_{}".format(self.__class__.TEST_ID),
                         "project name")

    def test_field_output_directory(self):
        self.assertEqual(self.__class__.project.output_directory,
                         directory("~/tests/test_{}".format(self.__class__.TEST_ID)),
                         "output directory")

    def test_field_title(self):
        self.assertEqual(self.__class__.project.title,
                         "test {} title".format(self.__class__.TEST_ID),
                         "project title")

    def test_field_brief(self):
        self.assertEqual(self.__class__.project.brief,
                         "test {} brief".format(self.__class__.TEST_ID),
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

    def get_project(cls):
        return self.project

if __name__ == "__main__":
    unittest.main()
