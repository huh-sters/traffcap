import re
from .rule_match import RuleMatch


class HeaderKeyRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_keys(self.request.headers, re.compile(self.pattern))
