import re
from .rule_match import RuleMatch


class DomainNameRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string(self.request.url.hostname, re.compile(self.pattern))
