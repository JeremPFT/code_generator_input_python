""" A Filter is used by a Template_Engine to transform given parameter.

Defined filters:

- Double
Repeat given string (used to test filter principle).

- Capitalize
Capitalize given string.

- Upper
Uppercase given string.
"""

class Filter():
    # trying to build a OOP filters family

    registered = {}

    def __init__(self, tag_name):
        self.tag_name = tag_name.lower()

    def process(self, tag_value):
        the_process = Filter.PROCESSING[self.index]
        return the_process(self, tag_value)

    def register(Filter_Class):
        registered[Filter_Class, Filter_Class.tag_name]


class Filter_Capitalize(Filter):
    def __init__(self):
        super().__init__("capitalize")
        Filter.register(self.__class__, self.tag_name)

    def process(self, tag_value):
        words = tag_value.split("_")
        splitted_image = []
        for word in words:
            splitted_image.append(word.capitalize())
        return "_".join(splitted_image)


class Filter_Upper(Filter):
    def __init__(self):
        super().__init__("upper")
        Filter.registered.append(self)

    def process(self, tag_value):
        return tag_value.upper()


class Filter_Double(Filter):
    def __init__(self):
        super().__init__("double")
        Filter.registered.append(self)

    def process(self, tag_value):
        result = ""
        for car in argument:
            result += car
            result += car
        return result
