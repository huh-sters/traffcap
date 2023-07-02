from typing import Optional
from .repository import Repository
from traffcap.model import Rule
from sqlalchemy import select, ScalarResult


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        session = await cls.new_session()
        return await session.get(Rule, rule_id)

    @classmethod
    async def get_all_rules(cls) -> ScalarResult[Rule]:
        session = await cls.new_session()
        return await session.scalars(select(Rule))

    @classmethod
    async def create_rule(cls, rule: str = ".*") -> Optional[Rule]:
        session = await cls.new_session()
        async with session.begin():
            new_rule = Rule(rule=rule)
            session.add(new_rule)

        return await cls.get_rule_by_id(new_rule.id)

    @classmethod
    async def delete_rule_by_id(cls, rule_id: int) -> None:
        session = await cls.new_session()
        async with session.begin():
            rule = await session.get(Rule, rule_id)
            await session.delete(rule)

    @classmethod
    async def find_matching_rules(cls, rule: str) -> ScalarResult[Rule]:
        """
        Find all rules that match this current rule
        """
        session = await cls.new_session()
        stmnt = select(Rule).where(Rule.rule == rule)
        return await session.scalars(stmnt)
