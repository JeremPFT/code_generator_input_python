import os

from src.uml_model import *
from src.utils import (indent, dbg, capitalize_identifier, build_dir)
from src.template_engine import Template_Engine


class Generator_Ada_Project():
    def __init__(self, template_engine):
        if template_engine.__class__ != Template_Engine:
            raise ValueError("template_engine must be of Template_Engine class")
        self.__template_engine = template_engine

    def output(self, project):
        self._output_project(project)

    def _output_project(self, project):
        if project.__class__.__name__ != "Project":
            raise TypeError("Project instance expected")

        prj_dir = os.path.normpath(project.output_directory())

        build_dir(prj_dir)
        os.chdir(prj_dir)
        build_dir("src")

        project_name = capitalize_identifier(project.name)

        print("project name: %s" % (project_name))

        te = self.__template_engine

        rendered_template = te.render (file_name    = "project.gpr",
                                       dico = {'project_name' : project_name})

        f = open(project.name + ".gpr", "w")
        f.write(rendered_template)
        f.close()

        print("file generated: ")
        print(rendered_template)
