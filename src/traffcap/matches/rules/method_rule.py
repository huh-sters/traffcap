import re
from .rule_match import RuleMatch


class MethodRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string(self.request.method, re.compile(self.pattern))
