import re
from .rule_match import RuleMatch


class ProtocolRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string(self.request.url.scheme, re.compile(self.pattern))
