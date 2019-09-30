import os

from indent import indent

class Named_Element:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        image = "<" + self.__class__.__name__ + "> name: '%s'" % (self.name)
        return image


class Project(Named_Element):
    def __init__(self, name, out_dir, package_list):
        super().__init__(name)
        self.out_dir      = out_dir
        self.package_list = package_list

    def __str__(self):
        image = os.linesep + "========================================" + os.linesep
        image += super().__str__() + os.linesep + "in %s" % (self.out_dir) + os.linesep
        indent.incr()
        for package in self.package_list:
            image += indent.str() + str(package)
        indent.decr()
        return image


class Package(Named_Element):
    def __init__(self, name, packageable_element_list):
        super().__init__(name)
        self.packageable_element_list = packageable_element_list

    def __str__(self):
        image = super().__str__() + os.linesep
        indent.incr()
        for element in self.packageable_element_list:
            image += indent.str() + str(element) + os.linesep
        indent.decr()
        return image


class Class(Named_Element):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        image = super().__str__()
        return image


class Subprogram(Named_Element):
    def __init__(self, name, parameter_list):
        super().__init__(name)
        self.parameter_list = parameter_list

    def __str__(self):
        image = super().__str__()
        indent.incr()
        for parameter in self.parameter_list:
            image += indent.str() + str(parameter) + os.linesep
        indent.decr()
        return image
