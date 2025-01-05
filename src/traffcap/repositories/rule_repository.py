from typing import Optional, Sequence
from .repository import Repository
from traffcap.model import Rule
from sqlalchemy import select


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        async with cls.session() as session:
            return await session.get(Rule, rule_id)
        
        return None

    @classmethod
    async def get_all_rules(cls) -> Sequence[Rule]:
        async with cls.session() as session:
            results = await session.scalars(
                select(Rule)
            )
            return results.all()

        return []

    @classmethod
    async def create_rule(cls, rule: str = ".*") -> Optional[Rule]:
        async with cls.session() as session:
            new_rule = Rule(rule=rule)
            session.add(new_rule)
            await session.commit()

            return new_rule

        return None

    @classmethod
    async def delete_rule_by_id(cls, rule_id: int) -> None:
        async with cls.session() as session:
            await session.delete(
                await session.get(Rule, rule_id)
            )
            await session.commit()

    @classmethod
    async def find_matching_rules(cls, rule: str) -> Sequence[Rule]:
        """
        Find all rules that match this current rule
        """
        # async with cls.session() as session:
        #     results = await session.scalars(
        #         select(Rule)
        #             .where(Rule.rule == rule)
        #     )
        #     return results.all()

        return []
