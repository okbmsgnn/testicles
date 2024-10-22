from __future__ import annotations

import functools
import time
import traceback
from typing import Callable, Dict, List, Optional

from testicles._assert import Assert
from testicles.exceptions import AssertException
from testicles.test_case.test_result import (ErrorTestResult, FailTestResult,
                                             SkipTestResult, SuccessTestResult,
                                             TestResult)


class TestCase:
    
    _fn: Callable | None
    _subtests: List[TestCase]

    _before_all: Optional[Callable]
    _before_each: Optional[Callable]
    _after_all: Optional[Callable]
    _after_each: Optional[Callable]

    _name_or_description: str
    @property    
    def name_or_description(self):
        return self._name_or_description

    _result: TestResult | None = None
    @property    
    def result(self):
        return self._result

    _assert: Assert
    @property    
    def assert_(self):
        return self._assert

    def __init__(self, name_or_description: str, /, fn: Callable | None) -> None:
        self._fn = fn
        self._subtests = []
        self._name_or_description = name_or_description
        self._assert = Assert()

    def _register_hook(self, fn: Callable, hook_name: str):
        key = f"_{hook_name}"

        if self.__getattribute__(key) is not None:
            raise Exception(f"\"{key}\" hook has been already registered.")

        self.__setattr__(key, fn)
        
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            fn(*args, **kwargs)
        
        return wrapper

    def before_all(self, fn: Callable):
        return self._register_hook(fn, self.before_all.__name__)
    
    def before_each(self, fn: Callable):
        return self._register_hook(fn, self.before_each.__name__)
    
    def after_all(self, fn: Callable):
        return self._register_hook(fn, self.after_all.__name__)
    
    def after_each(self, fn: Callable):
        return self._register_hook(fn, self.after_each.__name__)
    
    def skip(self, reason: str):
        self._result = SkipTestResult(reason)

    def subtest(self, name_or_description: str):
        def decorator(fn: Callable):
            test_case = TestCase(name_or_description, fn=fn)
            self._subtests.append(test_case)
            return fn

        return decorator

    def run(self, fn: Callable | None = None):
        if isinstance(self._result, SkipTestResult):
            return self._result
        elif self._result is not None:
            raise Exception("Test has been already run.")

        started_at = time.perf_counter()

        try:
            self._fn = self._fn or fn
            if self._fn is None:
                raise Exception("\"fn\" was not provided.")
            self._fn(self)
            for subtest in self._subtests:
                result = subtest.run()
                if isinstance(result, SuccessTestResult):
                    print(f"{subtest.name_or_description} | SUCCESS | {result.get_execution_ms():.4f}s")
                elif isinstance(result, FailTestResult):
                    print(f"{subtest.name_or_description} | FAIL    | {result.get_execution_ms():.4f}s")
                elif isinstance(result, ErrorTestResult):
                    description, error = result.get_full_description()
                    print(f"{subtest.name_or_description} | ERROR   | {result.get_execution_ms():.4f}s | {description} | {error}")
                    traceback.print_exception(error)

            ended_at = time.perf_counter()
            self._result = SuccessTestResult(started_at=started_at, ended_at=ended_at)
            return self._result
        except AssertException as e:
            ended_at = time.perf_counter()
            self._result = FailTestResult("", [], started_at=started_at, ended_at=ended_at)
            return self._result
        except Exception as e:
            ended_at = time.perf_counter()
            self._result = ErrorTestResult("", e, started_at=started_at, ended_at=ended_at)
            return self._result