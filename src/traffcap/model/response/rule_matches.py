from traffcap.model import RulePublic, MatchPublic


class RuleMatches(RulePublic, table=False):
    matches: list[MatchPublic] = []
