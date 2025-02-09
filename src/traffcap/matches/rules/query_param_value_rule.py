import re
from .rule_match import RuleMatch


class QueryParamValueRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_values(dict(self.request.query_params), re.compile(self.pattern))
