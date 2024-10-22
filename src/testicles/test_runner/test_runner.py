
from testicles.test_case import TestCase
from testicles.test_suite import TestSuite


class TestRunner:

    _suite: TestSuite

    def __init__(self, suite: TestSuite) -> None:
        self._suite = suite

    def run(self):
        self._on_suite_start(self._suite)

        for test_case, result in self._suite.run():
            if result is None:
                if test_case._parent is None:
                    self._on_test_start(test_case)
                else:
                    self._on_subtest_start(test_case)
            else:
                if test_case._parent is None:
                    self._on_test_end(test_case)
                else:
                    self._on_subtest_end(test_case)

        self._on_suite_end(self._suite)

    def _on_suite_start(self, suite: TestSuite):
        pass

    def _on_suite_end(self, suite: TestSuite):
        pass

    def _on_test_start(self, test: TestCase):
        pass

    def _on_test_end(self, test: TestCase):
        pass

    def _on_subtest_start(self, test: TestCase):
        pass

    def _on_subtest_end(self, test: TestCase):
        pass