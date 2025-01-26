import re
from .rule_match import RuleMatch


class QueryParamKeyRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_keys(self.request.query_params, re.compile(self.pattern))
