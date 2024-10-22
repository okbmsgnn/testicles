from unittest.mock import MagicMock, patch

from testicles.test_case import TestCase

from .sum import sum
from .unit_test import test_suite


@test_suite.test(name_or_description="sum()")
def test_sum(ctx: TestCase):

    @ctx.subtest(name_or_description="sums positive numbers")
    def sums_positive_numbers(ctx: TestCase):
        result = sum(3, 5)

        ctx.should.equal_to(8, result)

    @ctx.subtest(name_or_description="sums negative numbers")
    @patch("sandbox.sum.mapping")
    def sums_negative_numbers(ctx: TestCase, mapping: MagicMock):
        result = sum(-1, -6)
        
        ctx.should.equal_to(-7, result)