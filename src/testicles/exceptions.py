class AssertException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Assertion failed", *args)
        
class SkipTestException(Exception):
    reason: str
    
    def __init__(self, reason: str, *args: object) -> None:
        super().__init__("Test skipped", reason, *args)
        
        self.reason = reason