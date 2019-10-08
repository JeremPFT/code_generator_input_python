import os

from code_generator_utils import (
    indent,
    debug,
)

class Project:
    def __init__(self, name):
        self.name             = name
        self._output_directory = ""
        self._package_list     = []

    def set_output_directory(self, output_directory):
        self._output_directory = output_directory.replace('"', '')

    def add_package(self, package_item):
        self._package_list.append(package_item)
        package_item.project = self

    def __str__(self):
        image  = "<" + self.__class__.__name__ + "> '%s'" % (self.name) + os.linesep
        image += "in %s" % (self._output_directory) + os.linesep
        indent.incr()
        j = 1
        for package in self._package_list:
            image += indent.str() + str(package)
            j += 1
            if j <= len(self._package_list):
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
        self.project = None

    def __str__(self):
        image = super().__str__() + os.linesep
        if self.project == None:
            image += "no output file"
        else:
            image += "output file: %s" % (self.project._output_directory + "/src/" + self.name + ".ads")
        image += os.linesep
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

        self._is_abstract     = is_abstract
        self._dependance_list = []
        self._operation_list  = []
        self._property_list   = []
        self._owner           = owner

        self._parent = None

        if parent_name != None:
            if type(parent_name) != str:
                raise Exception("parent_name has to be a string")
            else:
                parent = owner.find_element(parent_name)
                if parent == None:
                    raise Exception("parent '%s' of '%s' not found in '%s'"
                                    % (parent_name, self.name, owner.name))

    def add_property(self, property_item):
        self._property_list.append(property_item)

        if property_item.of_type.endswith("_vector"):
            self.add_operation(Operation.create_vector_count(property_item))
            self.add_operation(Operation.create_vector_get_by_index(property_item))
            self.add_operation(Operation.create_vector_has_item(property_item))
            self.add_operation(Operation.create_vector_add_item(property_item))

    def add_operation(self, operation_item):
        self._operation_list.append(operation_item)

    def __dependance_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self._dependance_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self._dependance_list):
                image += os.linesep
        indent.decr()
        return image

    def __property_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self._property_list:
            # if self._parent != None and element in self._parent.property_list:
            #     pass
            # else:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self._property_list):
                image += os.linesep
        indent.decr()
        return image

    def __operation_list_image(self):
        image = ""
        indent.incr()
        j = 1
        for element in self._operation_list:
            image += indent.str() + str(element)
            j += 1
            if j <= len(self._operation_list):
                image += os.linesep
        indent.decr()
        return image

    def __str__(self):

        image = "-" * 50 + os.linesep + indent.str() + super().__str__()

        if self._parent != None:
            image += " extends %s" % (self._parent)

        if self._is_abstract:
            image += " is abstract"

        image += os.linesep
        image += self.__dependance_list_image()
        if len(self._dependance_list) > 0:
            image += os.linesep
        image += self.__property_list_image()
        if len(self._property_list) > 0 and len(self._operation_list) > 0:
            image += os.linesep
        image += self.__operation_list_image()

        return image


class Operation(Named_Element):
    '''
    define procedure or function
    '''

    def __init__(self, name, is_query = False):
        super().__init__(name)
        self._is_query = is_query
        self._parameter_list = []
        self._returned_parameter_list = []

    def add_parameter(self, parameter):
        if parameter.__class__ != Parameter:
            raise Exception("class Parameter expected. Got " + str(parameter))

        if parameter.is_return():
            self._returned_parameter_list.append(parameter)
        else:
            self._parameter_list.append(parameter)

    def __return_image(self):
        image = ""

        if len(self._returned_parameter_list) > 0:
            image += " return "

        if len(self._returned_parameter_list) > 1:
            image += ("(")

        for param in self._returned_parameter_list:
            image += param.of_type

            if param != self._returned_parameter_list[-1]:
                image += ", "

        if len(self._returned_parameter_list) > 1:
            image += (")")

        return image

    def __parameters_image(self):
        image = ""

        if len(self._parameter_list) == 0:
            return image

        indent.incr()

        for param in self._parameter_list:
            image += indent.str() + str(param)
            if param != self._parameter_list[-1]:
                image += os.linesep

        indent.decr()
        return image

    def __str__(self):
        image = super().__str__()

        image += self.__return_image()

        if len(self._parameter_list) > 0:
            image += os.linesep

        image += self.__parameters_image()

        return image

    @staticmethod
    def create_vector_count(property_item):
        operation = Operation(name = property_item.name + "_count")

        param_self = Parameter(name      = "self",
                               direction = Parameter.DIRECTION_IN,
                               of_type   = "object_t")

        param_return = Parameter(name      = "result",
                                 direction = Parameter.DIRECTION_RETURN,
                                 of_type   = "natural")

        for param in (param_self, param_return):
            operation._parameter_list.append(param)

        return operation

    @staticmethod
    def create_vector_get_by_index(property_item):
        operation = Operation(name = "get_" + property_item.name)

        param_self = Parameter(name      = "self",
                               direction = Parameter.DIRECTION_IN,
                               of_type   = "object_t")

        param_index = Parameter(name      = "index",
                                direction = Parameter.DIRECTION_IN,
                                of_type   = "positive")

        item_type = property_item.of_type.replace("_vector", "")
        param_return = Parameter(name      = "result",
                                 direction = Parameter.DIRECTION_RETURN,
                                 of_type   = item_type)

        for param in (param_self, param_index, param_return):
            operation._parameter_list.append(param)

        return operation

    @staticmethod
    def create_vector_has_item(property_item):
        operation = Operation(name = "has_" + property_item.name)

        param_self = Parameter(name      = "self",
                               direction = Parameter.DIRECTION_IN,
                               of_type   = "object_t")

        param_value = Parameter(name      = "value",
                                direction = Parameter.DIRECTION_IN,
                                of_type   = "object_t")

        param_return = Parameter(name      = "result",
                                 direction = Parameter.DIRECTION_RETURN,
                                 of_type   = "boolean")

        for param in (param_self, param_value, param_return):
            operation._parameter_list.append(param)

        return operation

    @staticmethod
    def create_vector_add_item(property_item):
        operation = Operation(name = "add_" + property_item.name)

        param_self = Parameter(name      = "self",
                               direction = Parameter.DIRECTION_INOUT,
                               of_type   = "object_t")

        param_value = Parameter(name      = "value",
                               direction = Parameter.DIRECTION_IN,
                               of_type   = property_item.of_type)

        for param in (param_self, param_value):
            operation._parameter_list.append(param)

        return operation


class Typed_Element(Named_Element):
    '''
    Element with a type (extended by Parameter and Property)
    '''
    def __init__(self, name, of_type, default = None):
        super().__init__(name)
        self.of_type = of_type
        self.default = default

    def __str__(self):
        image = super().__str__() + " : %s" % (self.of_type)
        if self.default != None:
            image += " := %s" % (self.default)
        return image

class Parameter(Typed_Element):
    '''
    Parameter of an operation
    '''

    DIRECTION_IN     = "in"
    DIRECTION_OUT    = "out"
    DIRECTION_INOUT  = "inout"
    DIRECTION_RETURN = "return"

    DIRECTIONS = [DIRECTION_IN, DIRECTION_OUT, DIRECTION_INOUT, DIRECTION_RETURN]

    def __init__(self, name, of_type, direction = None, default = None):
        if direction == None:
            direction = Parameter.DIRECTION_IN

        if not direction in Parameter.DIRECTIONS:
            raise Exception("unknown parameter direction: " + mode)

        super().__init__(name, of_type, default)
        self._direction = direction

    def __str__(self):
        image = super().__str__() + " [%s]" % (self._direction)
        if self.default != None:
            image += " := %s" % (self.default)
        return image

    def is_return(self):
        return self._direction == Parameter.DIRECTION_RETURN


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
