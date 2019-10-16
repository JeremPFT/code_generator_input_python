import os

from src.uml_model import *
from src.utils import (indent, dbg, capitalize_identifier, build_dir)
from src.template_engine import Template_Engine


class Generator_Ada_Project():
    def __init__(self, template_engine):
        if template_engine.__class__ != Template_Engine:
            raise TypeError("template_engine must be of Template_Engine class")
        self.__template_engine = template_engine
        self.__project = None

    def output(self, project):
        if project.__class__ != Project:
            raise TypeError("Project instance expected")

        self.__project = project
        self.__output_project()

    def __create_tree(self):
        prj_dir = os.path.normpath(self.__project.output_directory())
        build_dir(prj_dir)
        build_dir(os.path.join(prj_dir, "src"))

    def __output_project(self):
        self.__create_tree()

        cap_project_name = capitalize_identifier(self.__project.name)

        print("project name: %s" % (cap_project_name))

        te = self.__template_engine

        rendered_template = te.render (file_name    = "project.gpr",
                                       dico = {'project_name' : cap_project_name})

        f = open(self.__project.name + ".gpr", "w")
        f.write(rendered_template)
        f.close()

        print("file generated: ")
        print(rendered_template)
