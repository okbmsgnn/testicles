from typing import Callable, List

from testicles.test_case import TestCase


class TestSuite:
    _name: str
    _tests: List[TestCase]
    _cleanup_fns: List[Callable]

    def __init__(self, name: str) -> None:
        self._name = name
        self._tests = []
        self._cleanup_fns = []

    def test(self, name_or_description: str):
        def decorator(fn: Callable):
            test_case = TestCase(name_or_description, fn)
            self._tests.append(test_case)
            return fn

        return decorator

    def run(self):
        self.before_all()

        for test_case in self._tests:
            self.before_each()
            yield from test_case.run()
            self._run_cleanup()
            self.after_each()

        self.after_all()

    def before_each(self):
        pass

    def before_all(self):
        pass

    def after_each(self):
        pass

    def after_all(self):
        pass
    
    def add_cleanup(self, fn: Callable):
        self._cleanup_fns.append(fn)

    def _run_cleanup(self):
        for cleanup in self._cleanup_fns:
            try:
                cleanup()
            except Exception as e:
                print(e)
                
        self._cleanup_fns = []