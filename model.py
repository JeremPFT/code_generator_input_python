import os

from indent import indent


class Project:
    def __init__(self, name):
        self.name             = name
        self.output_directory = ""
        self.package_list     = []

    def __str__(self):
        image  = "<" + self.__class__.__name__ + "> '%s'" % (self.name) + os.linesep
        image += "in %s" % (self.output_directory) + os.linesep
        indent.incr()
        j = 1
        for package in self.package_list:
            image += indent.str() + str(package)
            j += 1
            if j <= len(self.package_list):
                image += os.linesep
        indent.decr()
        return image


class Named_Element:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        image = "<" + self.__class__.__name__ + "> '%s'" % (self.name)
        return image


class Namespace(Named_Element):
    def __init__(self, name):
        super().__init__(name)
        self.element_list = []

    def find_element(self, name):
        for element in self.element_list:
            if element.name == name:
                return element

        return None


class Package(Namespace):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        image = super().__str__() + os.linesep
        indent.incr()
        j = 1
        for element in self.element_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self.element_list):
                image += os.linesep
        indent.decr()
        return image

class Class(Namespace):
    def __init__(self, name, owner, parent_name = None, is_abstract = False):
        super().__init__(name)

        self.is_abstract     = is_abstract
        self.dependance_list = []
        self.operation_list  = []
        self.property_list   = []
        self.owner           = owner

        self.parent = None

        if parent_name != None:
            if type(parent_name) != str:
                raise Exception("parent_name has to be a string")
            else:
                parent = owner.find_element(parent_name)
                if parent == None:
                    raise Exception("parent '%s' of '%s' not found in '%s'"
                                    % (parent_name, self.name, owner.name))

    def __dependance_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self.dependance_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self.dependance_list):
                image += os.linesep
        indent.decr()
        return image

    def __property_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self.property_list:
            # if self.parent != None and element in self.parent.property_list:
            #     pass
            # else:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self.property_list):
                image += os.linesep
        indent.decr()
        return image

    def __operation_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self.operation_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self.operation_list):
                image += os.linesep
        indent.decr()
        return image

    def __str__(self):
        image = super().__str__()

        if self.parent != None:
            image += " extends %s" % (self.parent)

        if self.is_abstract:
            image += " is abstract"

        image += os.linesep
        image += self.__dependance_list_image()
        if len(self.dependance_list) > 0:
            image += os.linesep
        image += self.__property_list_image()
        if len(self.property_list) > 0 and len(self.operation_list) > 0:
            image += os.linesep
        image += self.__operation_list_image()

        return image


class Operation(Named_Element):

    '''define procedure or function'''

    def __init__(self, name, is_query = False):
        super().__init__(name)
        self.is_query = is_query
        self.parameter_list = []

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


class Typed_Element(Named_Element):
    def __init__(self, name, of_type, default):
        super().__init__(name)
        self.of_type = of_type
        self.default = default

    def __str__(self):
        image = super().__str__() + " : %s" % (self.of_type)
        if self.default != None:
            image += " := %s" % (self.default)
        return image


class Parameter(Typed_Element):

    DIRECTION_IN     = "in"
    DIRECTION_OUT    = "out"
    DIRECTION_INOUT  = "inout"
    DIRECTION_RETURN = "return"

    DIRECTIONS = [DIRECTION_IN, DIRECTION_OUT, DIRECTION_INOUT, DIRECTION_RETURN]

    def __init__(self, name, direction, of_type, default):
        if not direction in Parameter.DIRECTIONS:
            raise Exception("unknown parameter direction: " + mode)

        super.__init__(name)


class Property(Typed_Element):
    def __init__(self, name, of_type, default = None):
        super().__init__(name, of_type, default)
        self.of_type = of_type
        self.default = default

    def __str__(self):
        image = super().__str__()
        if self.default != None:
            image += " := %s" % (self.default)
        return image


class Dependance:

    MODE_WITH         = "with"
    MODE_USE          = "use"
    MODE_LIMITED_WITH = "limitedwith"

    MODES = [MODE_WITH, MODE_USE, MODE_LIMITED_WITH]

    def __init__(self, imported_unit, mode):
        if not mode in Dependance.MODES:
            raise Exception("unknown dependance mode: " + mode)

        self.imported_unit = imported_unit
        self.mode          = mode

    def __str__(self):
        image = "<" + self.__class__.__name__ + "> "

        if self.mode == Dependance.MODE_WITH:
            image += "with "
        elif self.mode == Dependance.MODE_USE:
            image += "use "
        elif self.mode == Dependance.MODE_LIMITED_WITH:
            image += "limited with "

        image += self.imported_unit

        return image
