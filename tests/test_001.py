import os

from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parser
from src.template_engine import Template_Engine

from src.utils import (
    directory,
    rmdir,
    dir_exists,
    text_files_match,
)

from tests.test_abstract import (
    Test_Abstract,
)

def check_project(test):
    name_valid = test.get_project().name == "test_001"
    output_directory_valid = test.get_project()._output_directory == directory("~/tests/test_001")
    return name_valid and output_directory_valid

def check_prj_dir(test):
    prj_dir = directory("~/tests/test_001")
    return dir_exists(prj_dir, "prj_dir")

def check_src_dir(test):
    src_dir = directory("~/tests/test_001/src")
    return dir_exists(src_dir, "src_dir")

def check_gpr_file(test):
    expected = "tests/test_001/test_001.gpr.expected"
    obtained = "~/tests/test_001/test_001.gpr"
    return text_files_match(expected = expected, obtained = obtained)

def failure(test):
    return False

class Test_001(Test_Abstract):
    def __init__(self):
        super().__init__()
        self.__project = None

    def _setup(self):
        super()._setup()

        input_data = open("tests/test_001/test_001.dsl", "r").read()

        self.__project = parser.parse(input_data, debug = False)

        template_engine = Template_Engine(template_directory = "tests/test_001")
        generator = Generator_Ada_Project(template_engine)
        generator.output(self.__project)

    def _setdown(self):
        super()._setdown()

    def _build_test_list(self):
        for test in (
                check_project,
                check_prj_dir,
                failure,
                check_src_dir,
                check_gpr_file,
        ):
            self._add_test(test)

    def get_project(self):
        return self.__project

Test_001().run()
