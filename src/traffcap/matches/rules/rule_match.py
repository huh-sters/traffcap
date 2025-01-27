from abc import ABC, abstractmethod
from typing import Optional
import re
from fastapi import Request


class RuleMatch(ABC):
    def __init__(self, request: Request, key: str, pattern: str, parent_id: int, invert: bool):
        self.request = request
        self.children: list["RuleMatch"] = []
        self.key = key
        self.pattern = pattern
        self.parent_id = parent_id
        self.invert = invert

    async def check_string(self, value: Optional[str], pattern: Optional[re.Pattern]) -> bool:
        if value is None or pattern is None:
            return False

        return pattern.search(value) is not None

    async def check_dictionary_keys(self, dictionary: Optional[dict], pattern: Optional[re.Pattern]) -> bool:
        if dictionary is None or pattern is None:
            return False

        for key in dictionary:
            if pattern.search(key) is not None:
                return True
        
        return False

    async def check_dictionary_values(self, dictionary: dict, pattern: Optional[re.Pattern]) -> bool:
        if pattern is None:
            return False

        for key in dictionary:
            if pattern.search(dictionary[key]) is not None:
                return True
        
        return False

    async def check_dictionary_value(self, dictionary: dict, key: Optional[str], pattern: Optional[re.Pattern]) -> bool:
        if key is None or pattern is None:
            return False

        return pattern.search(dictionary.get(key, "")) is not None

    @abstractmethod
    async def check(self) -> bool:
        ...
