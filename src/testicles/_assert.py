from typing import Any

from .exceptions import AssertException


class Assert:
    def equals_(self, expected: Any, actual: Any):
        if expected != actual:
            raise AssertException("Actual is not equal to the expected.")
        
    def in_(self, member: Any, container: Any):
        if member not in container:
            raise AssertException("Member was not found in the container.")

    def not_in_(self, member: Any, container: Any):
        if member in container:
            raise AssertException("Member was found in the container.")
    
    def is_(self, value1: Any, value2: Any):
        if value1 is not value2:
            raise AssertException("Values are not the same.")
    
    def is_not_(self, value1: Any, value2: Any):
        if value1 is not value2:
            raise AssertException("Values are the same.")
