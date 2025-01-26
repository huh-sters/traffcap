import re
from .rule_match import RuleMatch


class QueryParamKeyValueRule(RuleMatch):
    async def check(self) -> bool:
        return await self.check_dictionary_value(self.request.query_params, self.key, re.compile(self.pattern))
