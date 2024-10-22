from typing import List, Tuple


class TestResult:
    _started_at: float
    _ended_at: float

    def __init__(self, started_at: float, ended_at: float) -> None:
        self._started_at = started_at
        self._ended_at = ended_at
    
    def get_execution_ms(self) -> float:
        return self._ended_at - self._started_at

    def is_success(self) -> bool:
        raise Exception("Not implemented.")
    

class SuccessTestResult(TestResult):
    def is_success(self) -> bool:
        return True
    
class FailTestResult(TestResult):
    _description: str
    _messages: List[str] = []

    def __init__(self, description: str, messages: List[str], /, *, started_at: float, ended_at: float) -> None:
        super().__init__(started_at=started_at, ended_at=ended_at)
        
        self._description = description
        self._messages = messages

    def is_success(self) -> bool:
        return False
    
    def get_short_description(self) -> str:
        return self._description

    def get_full_description(self) -> Tuple[str, List[str]]:
        return (self._description, self._messages)
    
class ErrorTestResult(TestResult):
    _description: str
    _error: Exception

    def __init__(self, description: str, error: Exception, /, *, started_at: float, ended_at: float) -> None:
        super().__init__(started_at=started_at, ended_at=ended_at)
        
        self._description = description
        self._error = error 

    def is_success(self) -> bool:
        return False
    
    def get_short_description(self) -> str:
        return self._description

    def get_full_description(self) -> Tuple[str, Exception]:
        return (self._description, self._error)
    
class SkipTestResult(TestResult):
    _reason: str
    
    def __init__(self, reason: str) -> None:
        super().__init__(started_at=0, ended_at=0)
        
        self._reason = reason
    
    def get_reason(self) -> str:
        return self._reason
    
    def is_success(self) -> bool:
        return False