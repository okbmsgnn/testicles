class AssertException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Assertion failed", *args)