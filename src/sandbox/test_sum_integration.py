from testicles.test_case import TestCase

from .integration_test import test_suite


@test_suite.test(name_or_description="add()")
def test_add(ctx: TestCase):
    ctx.should.equal_to(1, 2)