from typing import Optional
from .repository import (
    Repository,
    inject_session
)
from traffcap.model import Rule
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession


class RuleRepository(Repository):
    @classmethod
    @inject_session
    async def get_rule_by_id(
        cls,
        rule_id: int,
        session: AsyncSession
    ) -> Optional[Rule]:
        return await session.get(Rule, rule_id)

    @classmethod
    @inject_session
    async def get_all_rules(
        cls,
        session: AsyncSession
    ) -> ScalarResult[Rule]:
        return await session.scalars(select(Rule))

    @classmethod
    @inject_session
    async def create_rule(cls, session: AsyncSession, rule: str = ".*") -> Rule:
        async with session.begin():
            new_rule = Rule(rule=rule)
            session.add(new_rule)

        return await cls.get_rule_by_id(new_rule.id)

    @classmethod
    @inject_session
    async def delete_rule_by_id(
        cls,
        rule_id: int,
        session: AsyncSession
    ) -> None:
        async with session.begin():
            rule = await session.get(Rule, rule_id)
            await session.delete(rule)

    @classmethod
    @inject_session
    async def find_matching_rules(
        cls,
        rule: str,
        session: AsyncSession
    ) -> ScalarResult[Rule]:
        """
        Find all rules that match this current rule
        """
        async with session.begin():
            stmnt = select(Rule).where(Rule.rule == rule)
            return await session.scalars(stmnt)
