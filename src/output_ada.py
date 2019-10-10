import os

from jinja2 import (
    Environment,
    FileSystemLoader,
    PackageLoader,
)
# https://palletsprojects.com/p/jinja/
#
# from jinja2 import Template

from src.uml_model import *
from src.utils import (indent, dbg, capitalize_identifier, build_dir)

class Output_Ada():
    def __init__(self):
        self.env = Environment(loader      = FileSystemLoader('templates'),
                               trim_blocks = True)

    def output(self, project):
        self._output_project(project)

    def _output_project(self, project):
        template = self.env.get_template('lib_project.gpr')

        print()
        prj_dir = os.path.normpath(project.output_directory())
        dbg("buildind directory " + prj_dir)

        print("build dir '%s'" % (prj_dir))
        build_dir(prj_dir)
        os.chdir(prj_dir)
        print("build dir '%s'" % ("src"))
        build_dir("src")

        rendered_template = template.render(project_name = capitalize_identifier(project.name))

        f = open(project.name + ".gpr", "w")
        f.write(rendered_template)
        f.close()

        print("file generated: ")
        print(rendered_template)
