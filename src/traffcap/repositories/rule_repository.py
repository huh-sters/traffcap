from typing import Optional, Sequence
from .repository import Repository
from traffcap.model import Rule, Match
from sqlmodel import select, func, col


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        async with cls.session() as session:
            return await session.get(Rule, rule_id)
        
        return None

    @classmethod
    async def get_all_rules(cls) -> Sequence[Rule]:
        async with cls.session() as session:
            return (await session.exec(select(Rule))).unique().all()

        return []

    @classmethod
    async def get_all_rules_by_priority(cls) -> Sequence[Rule]:
        async with cls.session() as session:
            return (await session.exec(select(Rule).order_by(col(Rule.priority)))).unique().all()

        return []

    @classmethod
    async def get_lowest_priority(cls) -> int:
        async with cls.session() as session:
            result = (await session.exec(select(func.max(Rule.priority)))).first()
            if result:
                return result
        return 0


    @classmethod
    async def create_rule(cls, name: str = ".*", priority: int = 0, content_type: str = "", template: str = "") -> Optional[Rule]:
        async with cls.session() as session:
            new_rule = Rule(name=name, priority=priority, content_type=content_type, template=template)
            session.add(new_rule)
            await session.commit()

            return new_rule

        return None

    @classmethod
    async def add_match(cls, match: Match) -> Optional[Match]:
        async with cls.session() as session:
            session.add(match)
            await session.commit()

            return match

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

    @classmethod
    async def clear_all_rules(cls) -> None:
        """
        Remove all rules and matches from the database
        """
        async with cls.session() as session:
            await session.delete(Match)
            await session.delete(Rule)
            await session.commit()
