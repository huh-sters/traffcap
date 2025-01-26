import re
from .rule_match import RuleMatch


class PortRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string(str(self.request.url.port), re.compile(self.pattern))
