from __future__ import annotations

import functools
import time
from typing import Callable, Generator, List, Optional, Tuple

from testicles._assert import Assert
from testicles.exceptions import AssertException
from testicles.test_case.test_result import (ErrorTestResult, FailTestResult,
                                             SkipTestResult, SuccessTestResult,
                                             TestResult)


class TestCase:
    
    _parent: TestCase | None
    _fn: Callable
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

    _should: Assert
    @property
    def should(self):
        return self._should

    def __init__(self, name_or_description: str, fn: Callable, /, *, parent: TestCase | None = None) -> None:
        self._fn = fn
        self._parent = parent
        self._subtests = []
        self._name_or_description = name_or_description
        self._should = Assert()

    def _get_full_name(self):
        parts = [self._name_or_description]

        parent = self._parent
        while parent is not None:
            parts.insert(0, parent._name_or_description)
            parent = parent._parent
            
        return parts

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

    def subtest(self, fn: Callable | None = None, /, *, name_or_description: str | None = None):
        def decorator(fn: Callable):
            test_case = TestCase(name_or_description or fn.__name__, fn, parent=self)
            self._subtests.append(test_case)
            return fn

        if fn is None:
            return decorator

        return decorator(fn)

    def run(self) -> Generator[Tuple[TestCase, TestResult | None], None, Tuple[TestCase, TestResult | None]]:
        if isinstance(self._result, SkipTestResult):
            return (self, self._result)
        elif self._result is not None:
            raise Exception("Test has been already run.")

        yield (self, None)

        started_at = time.perf_counter()

        try:
            self._fn(self)
            for subtest in self._subtests:
                yield from subtest.run()

            ended_at = time.perf_counter()
            self._result = SuccessTestResult(started_at=started_at, ended_at=ended_at)
        except AssertException as e:
            ended_at = time.perf_counter()
            self._result = FailTestResult("", [], started_at=started_at, ended_at=ended_at)
        except Exception as e:
            ended_at = time.perf_counter()
            self._result = ErrorTestResult("", e, started_at=started_at, ended_at=ended_at)

        return (self, self._result)