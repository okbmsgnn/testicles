
from testicles.test_case import TestCase
from testicles.test_suite import TestSuite

TAB = "  "

class TestRunner:

    _suite: TestSuite

    def __init__(self, suite: TestSuite) -> None:
        self._suite = suite

    def run(self):
        self.__on_suite_start(self._suite)
        
        for test_case, result in self._suite.run():
            if result is None:
                if test_case._parent is None:
                    self.__on_test_start(test_case)
                else:
                    self.__on_test_end(test_case)
            else:
                if test_case._parent is None:
                    self.__on_subtest_start(test_case)
                else:
                    self.__on_subtest_end(test_case)

        self.__on_suite_end(self._suite)

    def __on_suite_start(self, suite: TestSuite):
        print("test [%s] {" % suite._name)

    def __on_suite_end(self, suite: TestSuite):
        print("}")

    def __on_test_start(self, test: TestCase):
        print(f"{TAB}{test.name_or_description}")

    def __on_test_end(self, test: TestCase):
        pass

    def __on_subtest_start(self, test: TestCase):
        parent = test
        nesting_level = 1
        while parent is not None:
            nesting_level += 1
            parent = test._parent
        
        print(f"{TAB * nesting_level} {test.name_or_description}")

    def __on_subtest_end(self, test: TestCase):
        pass