from src.utils import (
    rmdir,
)

class Test_Abstract:
    def __init__(self):
        self.__test_ok_list = []
        self.__test_ko_list = []
        self.__test_list = []

    def _add_test(self, impl):
        self.__test_list.append(impl)

    def _test(self, test):
        if test(self):
            self._works(test)
        else:
            self._fails(test)

    def _works(self, test):
        self.__test_ok_list.append(test)
        print("test " + str(test.__name__) + ": OK")

    def _fails(self, test):
        self.__test_ko_list.append(test)
        print("test " + str(test) + ": KO")

    def _setup(self):
        pass

    def _setdown(self):
        rmdir("~/tests")

    def _build_test_list(self):
        pass

    def run(self):
        print("\n========== CAMPAIGN %s ==========\n" % (self.__class__.__name__))

        self._setup()
        self._build_test_list()
        for test in self.__test_list:
            self._test(test)

        print("\n---------- RESULT ----------\n")

        print("tests count: " + str(len(self.__test_list)))
        print("tests ok:    " + str(len(self.__test_ok_list)))
        print("tests ko:    " + str(len(self.__test_ko_list)))
        print()

        for test in self.__test_ok_list:
            print("test " + test.__name__ + " OK")

        print()

        for test in self.__test_ko_list:
            print("test " + test.__name__ + " KO")

        self._setdown()
