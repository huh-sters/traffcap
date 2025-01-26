import re
from .rule_match import RuleMatch


class BodyRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string((await self.request.body()).decode("utf-8"), re.compile(self.pattern))
