import unittest

from src.uml_model import *

class Test_Project(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setup class " + cls.__name__)

    @classmethod
    def tearDownClass(cls):
        print("teardown class " + cls.__name__)

    def setUp(self):
        print("setup instance")

    def tearDown(self):
        print("teardown instance")

    def test_init(self):
        name = "project_name"
        output_directory = ""

        expected = { "name" : name,
                      "output_directory" : output_directory}

        project = Project(name)

        field = "name"
        self.assertEqual(getattr(project, field),
                         expected[field],
                         "field " + field
                         )

        field = "output_directory"
        self.assertEqual(getattr(project, field),
                         expected[field],
                         "field " + field
                         )

        # field = "output_directory"
        # self.assertEqual(project.__dict__[field],
        #                  expected[field],
        #                  field)

unittest.main()
