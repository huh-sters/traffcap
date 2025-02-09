import re
from .rule_match import RuleMatch


class HeaderValueRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_values(dict(self.request.headers), re.compile(self.pattern))
