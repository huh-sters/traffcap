from .rule_match import RuleMatch


class RootRule(RuleMatch):
    """
    Pseudo node that always returns true at the root of the tree
    """
    async def check(self) -> bool:
        return True
