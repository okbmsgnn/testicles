import functools
import traceback
from typing import Callable, List

from testicles.test_case import (ErrorTestResult, FailTestResult,
                                 SuccessTestResult, TestCase, TestResult)


class TestSuite:
    _name: str
    _tests: List[TestCase] = []

    def __init__(self, name: str) -> None:
        self._name = name

    def test(self, name_or_description: str):
        def decorator(fn: Callable):
            test_case = TestCase(name_or_description, fn=fn)
            self._tests.append(test_case)
            return fn

        return decorator
    
    def run(self):
        for test_case in self._tests:
            result = test_case.run()

            if isinstance(result, SuccessTestResult):
                print(f"{test_case.name_or_description} | SUCCESS | {result.get_execution_ms():.4f}s")
            elif isinstance(result, FailTestResult):
                print(f"{test_case.name_or_description} | FAIL    | {result.get_execution_ms():.4f}s")
            elif isinstance(result, ErrorTestResult):
                description, error = result.get_full_description()
                print(f"{test_case.name_or_description} | ERROR   | {result.get_execution_ms():.4f}s | {description} | {error}")
                traceback.print_exception(error)