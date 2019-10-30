'''
source to create decorators:

https://www.codementor.io/sheena/advanced-use-python-decorators-class-function-du107nxsv
https://stackoverflow.com/questions/9125832/how-can-i-add-properties-to-a-class-using-a-decorator-that-takes-a-list-of-names
'''

import logging

def logged(level):
    def add_log(Cls):
        class Logged_Class(Cls):
            def __init__(self, *args, **kwargs):
                log_name = Cls.__name__
                self.log = logging.getLogger(log_name)
                self.log.setLevel(level)
                self.log.info("initialize Logged_Class instance")

            def __getattribute__(self, attr):
                try:
                    x = super(Logged_Class, self)
                self.log.fatal("getting attribute")
        return Logged_Class
    return add_log

@logged("DEBUG")
class Essai:

    def __init__(self):
        self.log.fatal("initialize Essai instance")


essai = Essai()
