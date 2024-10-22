
from testicles.test_case import TestCase
from testicles.test_case.test_result import (ErrorTestResult, FailTestResult,
                                             SkipTestResult, SuccessTestResult)
from testicles.test_runner import TestRunner
from testicles.test_suite import TestSuite

TAB = "  "

class TextTestRunner(TestRunner):
    
    def __init__(self, suite: TestSuite) -> None:
        super().__init__(suite)

    def _on_suite_start(self, suite: TestSuite):
        print("suite [%s] {" % suite._name)

    def _on_suite_end(self, suite: TestSuite):
        print("}")

    def _on_test_start(self, test: TestCase):
        print(f"{TAB}test [{test.name_or_description}] {{")

    def _on_test_end(self, test: TestCase):
        nesting_level = 1

        if isinstance(test.result, SkipTestResult):
            print(f"{TAB*(nesting_level+1)}SKIP    | {test.result.get_execution_ms():.4f}s | {test.result.get_reason()}")
        elif isinstance(test.result, SuccessTestResult):
            print(f"{TAB*(nesting_level+1)}SUCCESS | {test.result.get_execution_ms():.4f}s")
        elif isinstance(test.result, FailTestResult):
            _, messages = test.result.get_full_description()
            print(f"{TAB*(nesting_level+1)}FAIL    | {test.result.get_execution_ms():.4f}s | {messages}")
        elif isinstance(test.result, ErrorTestResult):
            _, error = test.result.get_full_description()
            print(f"{TAB*(nesting_level+1)}ERROR   | {test.result.get_execution_ms():.4f}s | {error}")

        print(f"{TAB}}}")

    def _on_subtest_start(self, test: TestCase):
        parent = test
        nesting_level = 0
        while parent is not None:
            nesting_level += 1
            parent = parent._parent

        print(f"{TAB * nesting_level}test [{test.name_or_description}] {{")

    def _on_subtest_end(self, test: TestCase):
        parent = test
        nesting_level = 0
        while parent is not None:
            nesting_level += 1
            parent = parent._parent

        if isinstance(test.result, SkipTestResult):
            print(f"{TAB*(nesting_level+1)}SKIP    | {test.result.get_execution_ms():.4f}s | {test.result.get_reason()}")
        elif isinstance(test.result, SuccessTestResult):
            print(f"{TAB*(nesting_level+1)}SUCCESS | {test.result.get_execution_ms():.4f}s")
        elif isinstance(test.result, FailTestResult):
            _, messages = test.result.get_full_description()
            print(f"{TAB*(nesting_level+1)}FAIL    | {test.result.get_execution_ms():.4f}s | {messages}")
        elif isinstance(test.result, ErrorTestResult):
            _, error = test.result.get_full_description()
            print(f"{TAB*(nesting_level+1)}ERROR   | {test.result.get_execution_ms():.4f}s | {error}")

        print(f"{TAB*nesting_level}}}")