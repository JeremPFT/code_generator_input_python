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

from tests.test_abstract import (
    Test_Abstract,
)

def no_name_project(test):
    try:
        test.__project = parser.parse(test.input_data, debug = False)
    except NoNameError as err:
        print(str(err))
        return True
    return False

class Test_002(Test_Abstract):
    def __init__(self):
        super().__init__()
        self.__project = None

    def _setup(self):
        super()._setup()

        self.input_data = open("tests/test_002/test_002.dsl", "r").read()

    def _setdown(self):
        pass

    def _build_test_list(self):
        for test in (
                no_name_project,
        ):
            self._add_test(test)

    def get_project(self):
        return self.__project

Test_002().run()
