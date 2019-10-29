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

import test_001

class Test_Project_Nominal_003(test_001.Test_Project_Nominal_001):

    TEST_ID = "003"

if __name__ == "__main__":
    unittest.main()
