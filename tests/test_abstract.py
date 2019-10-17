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

    def _fails(self, test):
        self.__test_ko_list.append(test)

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

        self._setdown()

        print("\n========== %s RESULTS ==========\n" % (self.__class__.__name__))

        print("Total Tests Run: " + str(len(self.__test_list)))

        print("\nSuccessful Tests: " + str(len(self.__test_ok_list)))

        for test in self.__test_ok_list:
            print("  Test " + test.__name__)

        print("\nFailed Tests: " + str(len(self.__test_ko_list)))

        for test in self.__test_ko_list:
            print("  Test " + test.__name__)

        print("\n========== %s END ==========\n" % (self.__class__.__name__))
