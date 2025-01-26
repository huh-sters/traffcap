import re
from .rule_match import RuleMatch
from traffcap.config import settings


class EndpointRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_string(self.request.url.path, re.compile(fr"^/{settings.requests_prefix}/{self.pattern}"))
