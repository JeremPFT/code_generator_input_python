import os
import logging

from src.utils import (
    indent,
    directory,
)

class NoNameError(Exception):
    pass


class Project:
    TYPE_STATIC_LIB = "static_library"
    TYPE_EXEC       = "executable"
    TYPE_TEST       = "test"

    TYPES = [TYPE_STATIC_LIB, TYPE_EXEC, TYPE_TEST]

    def __init__(self, name):
        logging.basicConfig(level=logging.DEBUG)
        self.log = logging.getLogger(__name__)

        assert type(name) == str, \
            "name is not a string {name!r}"
        assert name != "", "name is empty"

        self.name              = name
        self._output_directory = ""
        self._type             = ""
        self._title            = ""
        self._brief            = ""
        self._package_list     = []

    def output_directory(self):
        return self._output_directory

    def set_output_directory(self, output_directory):
        assert type(output_directory) == str, \
            "output directory has to be a string"

        dir = output_directory.replace('"', '')
        self._output_directory = directory(dir)

    def set_type(self, prj_type):
        assert prj_type in Project.TYPES, \
            "unknown project type: " + prj_type

        self._type = prj_type

    def set_title(self, title):
        assert type(title) == str, \
            "title has to be a string"

        self._title = title.replace('"', '')

    def set_brief(self, brief):
        if type(brief) != str:
            raise Exception("brief has to be a string")

        self._brief = brief.replace('"', '')

    def add_package(self, package_item):
        self._package_list.append(package_item)
        # package_item.project = self

    def __str__(self):
        image  = "<{self.__class__.__name__}> {self.name!r}".format(self=self) + os.linesep
        image += "in %s" % (self._output_directory) + os.linesep
        image += "title {!r}".format(self._title) + os.linesep
        image += "brief {!r}".format(self._brief) + os.linesep
        indent.incr()
        j = 1
        for package in self._package_list:
            image += indent.str() + str(package)
            j += 1
            if j <= len(self._package_list):
                image += os.linesep
        indent.decr()
        return image


class Element:
    '''
    see UML 2.4.1 Infrastructure section 9.15.1
    '''

    def __init__(self, owner = None, must_be_owned = False):
        if owner == self:
            raise ValueError("an element can not own itself")

        if must_be_owned and (owner == None):
            raise ValueError("the element must be owned")

        self.owner         = owner
        self.owned_element = []
        self.owned_comment = []
        self.must_be_owned = must_be_owned

    def add_owned_element(self, element):
        assert element != None and type(element) == Element, \
            "element has to be an Element instance"
        self.owned_element.append(element)

    def add_owned_comment(self, comment):
        assert comment != None and type(comment) == Comment, \
            "comment has to be an Comment instance"
        self.owned_comment.append(comment)

    def all_owned_element(self):
        result = []

        for element in self.owned_element:
            result.append(element)
            result.append(element.all_owned_element)

        return result

    def __str__(self):
        return "<{" + self.__class__.__name__ + "}>"

class Comment(Element):
    '''
    see UML 2.4.1 Infrastructure section 9.5
    '''

    def __init__(self, annoted_element = []):
        super.__init__()


class Multiplicity(Element):
    '''
    see UML 2.4.1 Infrastructure section 9.12
    '''

    def __init__(self,
                 is_ordered = False,
                 is_unique = True,
                 lower = 1,
                 upper = 1):

        assert type(is_ordered) == bool, \
            "is_ordered must be a boolean"

        assert type(is_ordered) == bool, \
            "is_ordered must be a boolean"

        assert lower == None or type(lower) == int, \
            "lower must be an integer"

        assert lower == None or lower >= 0, \
            "lower must be positive"

        assert upper == None or type(upper) == int, \
            "upper must be an integer"

        assert upper == None or ( lower != None and upper >= lower ), \
            "upper must greater than lower"

        self.is_ordered = is_ordered
        self.is_unique  = is_unique
        self.lower      = lower
        self.upper      = upper


class Named_Element(Element):
    '''
    see UML 2.4.1 Infrastructure section 9.14.1

    we ignore the possibility of no name or empty name
    '''

    def __init__(self, name, owner = None, must_be_owned = False):
        print("Named_Element, owner: " + str(owner))

        assert type(name) == str, \
            "name has to be a string"
        assert name != "", \
            "name has to be a no empty string"
        assert owner == None or Namespace in owner.__class__.__mro__, \
            "owner has to be a Namespace"
        assert type(must_be_owned) == bool, \
            "must_be_owned has to be a Boolean"


        super().__init__(owner = owner,
                         must_be_owned = must_be_owned)

        self.name = name

        self.qualified_name = name
        parent = self.owner
        while parent != None:
            self.qualified_name = parent.name + self.separator() + self.qualified_name
            parent = parent.owner

        if owner == None:
            print("building {0} without owner".format(self))
        else:
            print("building {0} with owner = {1.name}".format(self, owner))

    def __str__(self):
        return super().__str__() + "{0.qualified_name!r}".format(self)

    def separator(self):
        'return separator used to form qualified name'
        return "::"


class VisibilityKind():
    PUBLIC = 0
    PRIVATE = 1
    PROTECTED = 2
    PACKAGE = 3

    def __init__(self, value):
        assert value == PUBLIC \
            or value == PROTECTED \
            or value == PRIVATE \
            or value == PACKAGE, \
            'unknown visibility: ' + str(value)

        self.value

    def __str__(self):
        if self.value == PUBLIC:
            return "+"
        elif self.value == PRIVATE:
            return "-"
        elif self.value == PROTECTED:
            return "#"
        elif self.value == PACKAGE:
            return "~"

class Namespace(Named_Element):
    def __init__(self, name, owner = None):
        super().__init__(name, owner)
        self._member = []
        self._owned_member = []

    def find_element(self, name):
        for element in self._owned_member_list:
            if element.name == name:
                return element

        return None

    def add_owned_member(self, member):
        if member == None:
            raise Exception("member to add is None")

        self._owned_member_list.append(member)


class Package(Namespace):
    def __init__(self, name):
        super().__init__(name)
        # self.project = None

    def __str__(self):
        image = super().__str__() + os.linesep

        # if self.project == None:
        #     image += "no output file"
        # else:
        #     image += "output file: %s" %  \
        #     (self.project._output_directory \
        #      + "/src/" + self.name + ".ads")

        image += os.linesep

        indent.incr()

        for element in self._owned_member_list:
            image += indent.str() + str(element)

            if element != self._owned_member_list[-1]:
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
    '''
    see UML 2.4.1 Infrastructure section 11.3.5

    note
    if a property is owned by a class, it is an /attribute/ of the class
    '''

    def __init__(self, name, of_type, default = None):
        super().__init__(name, of_type, default)
        self.of_type = of_type
        self.default = default
        self.owning_class = None
        self.is_ordered = False
        self.is_unique = False

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


print("========================================")
print("== TEST MODEL")
nm_1 = Namespace("nm_1")
nm_2 = Namespace(name = "nm_2", owner = nm_1)
print(str(nm_1))
print(str(nm_2))
