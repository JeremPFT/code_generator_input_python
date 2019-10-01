import os

from indent import indent

class Named_Element:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        image = "<" + self.__class__.__name__ + "> '%s'" % (self.name)
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
        j = 1
        for package in self.package_list:
            image += indent.str() + str(package)
            j += 1
            if j <= len(self.package_list):
                image += os.linesep
        indent.decr()
        return image


class Package(Named_Element):
    def __init__(self, name, packageable_element_list):
        super().__init__(name)
        self.packageable_element_list = packageable_element_list

    def __str__(self):
        image = super().__str__() + os.linesep
        indent.incr()
        j = 1
        for element in self.packageable_element_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self.packageable_element_list):
                image += os.linesep
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
        if len(self.parameter_list) > 0:
            image += os.linesep
        j = 1
        for parameter in self.parameter_list:
            image += indent.str() + str(parameter)
            j += 1
            if j <= len(self.parameter_list):
                image += os.linesep
        indent.decr()
        return image


class Procedure(Subprogram):
    def __init__(self, name, parameter_list):
        super().__init__(name, parameter_list)


class Function(Subprogram):
    def __init__(self, name, returned_type, parameter_list):
        super().__init__(name, parameter_list)


class Typed_Element(Named_Element)
    def __init__(self, name, of_type, default):
        super().__init__(name)
        self.of_type = of_type
        self.default = default

    def __str__(self):
        image = super().__str__() + " : %s" % (self.of_type)
        if default != None:
            image += " := %s" % (self.default)
        return image

class Parameter(Typed_Element):
    pass

class Field(Typed_Element):
    pass
