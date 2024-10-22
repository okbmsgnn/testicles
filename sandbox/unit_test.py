from unittest.mock import MagicMock, patch

from src.testicles.test_case import TestCase
from src.testicles.test_suite import TestSuite

from .sum import sum

test_suite = TestSuite("unit")


@test_suite.test(name_or_description="sum()")
def test_sum(ctx: TestCase):

    @ctx.subtest(name_or_description="sums positive numbers")
    def sums_positive_numbers(ctx: TestCase):
        result = sum(3, 5)

        ctx.assert_.equals_(8, result)

    @ctx.subtest(name_or_description="sums negative numbers")
    @patch("sandbox.sum.mapping")
    def sums_negative_numbers(ctx: TestCase, mapping: MagicMock):
        result = sum(-1, -6)
        
        ctx.assert_.equals_(-7, result)

test_suite.run()