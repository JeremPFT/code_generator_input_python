import os

from src.uml_model import *
from src.template_engine import Template_Engine
from src.utils import (
    indent,
    dbg,
    capitalize_identifier,
    build_dir,
    directory,
)


class Generator_Ada_Project():
    def __init__(self, template_engine):
        if template_engine.__class__ != Template_Engine:
            raise TypeError("template_engine must be of Template_Engine class")
        self.__template_engine = template_engine
        self.__project = None

    def output(self, project):
        print(str(project))

        assert project != None and type(project) == Project, \
            "not a Project instance: " + str(type(project))

        if project == None:
            print("project is null, error during parsing")
            return

        self.__project = project
        self.__output_project()

    def __create_tree(self):
        prj_dir = directory(self.__project.output_directory)
        build_dir(prj_dir)
        build_dir(os.path.join(prj_dir, "src"))

    def __output_project(self):
        self.__create_tree()

        cap_project_name = capitalize_identifier(self.__project.name)

        te = self.__template_engine

        dico = {'project_name' : cap_project_name}
        tmpl_name = "project.gpr"
        rendered_template = te.render (file_name = tmpl_name,
                                       dico = dico)

        prj_dir = directory(self.__project.output_directory)
        gpr_file_name = self.__project.name + ".gpr"
        gpr_file_name = os.path.join(prj_dir, gpr_file_name)
        f = open(gpr_file_name, "w")
        f.write(rendered_template)
        f.close()
