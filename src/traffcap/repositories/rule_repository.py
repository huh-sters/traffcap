from typing import Optional
from .repository import Repository
from traffcap.model import Rule
from sqlalchemy import select, ScalarResult


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        rule = None
        async with cls.session() as session:
            rule = await session.get(Rule, rule_id)

        return rule

    @classmethod
    async def get_all_rules(cls) -> ScalarResult[Rule]:
        async with cls.session() as session:
            return await session.scalars(select(Rule))

    @classmethod
    async def create_rule(cls, rule: str = ".*") -> Optional[Rule]:
        return_rule = None
        async with cls.session() as session:
            async with session.begin():
                new_rule = Rule(rule=rule)
                session.add(new_rule)

            return_rule = await cls.get_rule_by_id(new_rule.id)

        return return_rule

    @classmethod
    async def delete_rule_by_id(cls, rule_id: int) -> None:
        async with cls.session() as session:
            async with session.begin():
                rule = await session.get(Rule, rule_id)
                await session.delete(rule)

    @classmethod
    async def find_matching_rules(cls, rule: str) -> ScalarResult[Rule]:
        """
        Find all rules that match this current rule
        """
        async with cls.session() as session:
            stmnt = select(Rule).where(Rule.rule == rule)
            return await session.scalars(stmnt)
