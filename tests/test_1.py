from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parser
from src.template_engine import Template_Engine

input_data = open("tests/test_1/test_1.dsl", "r").read()

project = parser.parse(input_data, debug = False)
print(str(project))

template_engine = Template_Engine(template_directory = "tests/test_1")
generator = Generator_Ada_Project(template_engine)
generator.output(project)
