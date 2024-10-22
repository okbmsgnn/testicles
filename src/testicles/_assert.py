from typing import Any

from .exceptions import AssertException


class Assert:
    def equal_to(self, expected: Any, actual: Any):
        if expected != actual:
            raise AssertException("Actual is not equal to the expected.")

    def not_equal_to(self, expected: Any, actual: Any):
        if expected == actual:
            raise AssertException("Actual is equal to the expected.")
        
    def be_in(self, member: Any, container: Any):
        if member not in container:
            raise AssertException("Member was not found in the container.")

    def not_be_in(self, member: Any, container: Any):
        if member in container:
            raise AssertException("Member was found in the container.")
    
    def be(self, value1: Any, value2: Any):
        if value1 is not value2:
            raise AssertException("Values are not the same.")
    
    def not_be(self, value1: Any, value2: Any):
        if value1 is not value2:
            raise AssertException("Values are the same.")
