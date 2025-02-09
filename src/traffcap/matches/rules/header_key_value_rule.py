import re
from .rule_match import RuleMatch


class HeaderKeyValueRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_value(dict(self.request.headers), self.key, re.compile(self.pattern))
