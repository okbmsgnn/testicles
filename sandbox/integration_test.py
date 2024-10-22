from src.testicles.test_case import TestCase
from src.testicles.test_suite import TestSuite

test_suite = TestSuite("integration")


@test_suite.test(name_or_description="add()")
def test_add(ctx: TestCase):
    ctx.assert_.equals_(1, 2)