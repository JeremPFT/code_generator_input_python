from src.generator_ada_project import Generator_Ada_Project
from src.dsl_grammar import parser
from src.template_engine import Template_Engine

input_data = open("tests/test_1.dsl", "r").read()

project = parser.parse(input_data, debug = False)
print(str(project))

directory = "~/Dropbox/projets_perso/ada/code_generator_py/tests/test_1/"

template_engine = Template_Engine(template_directory = directory)
generator = Generator_Ada_Project(template_engine)
generator.output(project)
