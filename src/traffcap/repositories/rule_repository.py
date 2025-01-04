from typing import Optional
from .repository import Repository
from traffcap.dto import Rule
from traffcap.model import RuleModel
from sqlalchemy import select


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        async with cls.session() as session:
            return Rule.model_validate(
                await session.get(RuleModel, rule_id)
            )
        
        return None

    @classmethod
    async def get_all_rules(cls) -> list[Rule]:
        rules = []
        async with cls.session() as session:
            results = await session.scalars(
                select(RuleModel)
            )
            for rule in results.all():
                rules.append(Rule.model_validate(rule))

        return rules

    @classmethod
    async def create_rule(cls, rule: str = ".*") -> Optional[Rule]:
        async with cls.session() as session:
            new_rule = RuleModel(rule=rule)
            session.add(new_rule)
            await session.commit()

            return Rule.model_validate(
                await cls.get_rule_by_id(new_rule.id)
            )

        return None

    @classmethod
    async def delete_rule_by_id(cls, rule_id: int) -> None:
        async with cls.session() as session:
            await session.delete(
                await session.get(RuleModel, rule_id)
            )
            await session.commit()

    @classmethod
    async def find_matching_rules(cls, rule: str) -> list[Rule]:
        """
        Find all rules that match this current rule
        """
        rules: list[Rule] = []
        # async with cls.session() as session:
        #     results = await session.scalars(
        #         select(RuleModel)
        #             .where(RuleModel.rule == rule)
        #     )
        #     for rule_item in results.all():
        #         rules.append(Rule.model_validate(rule_item))

        return rules
