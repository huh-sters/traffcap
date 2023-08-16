from typing import Optional
from .repository import Repository
from traffcap.dto import Rule
from traffcap.model import RuleModel
from sqlalchemy import select
from typing import List


class RuleRepository(Repository):
    @classmethod
    async def get_rule_by_id(cls, rule_id: int) -> Optional[Rule]:
        async with cls.session() as session:
            rule = await session.get(RuleModel, rule_id)
            return Rule.model_validate(rule)
        
        return None

    @classmethod
    async def get_all_rules(cls) -> List[Rule]:
        rules = []
        async with cls.session() as session:
            results = await session.scalars(select(RuleModel))
            for rule in results.all():
                rules.append(Rule.model_validate(rule))

        return rules

    @classmethod
    async def create_rule(cls, rule: str = ".*") -> Optional[Rule]:
        async with cls.session() as session:
            async with session.begin():
                new_rule = RuleModel(rule=rule)
                session.add(new_rule)

            return_rule = await cls.get_rule_by_id(new_rule.id)
            return Rule.model_validate(return_rule)

        return None

    @classmethod
    async def delete_rule_by_id(cls, rule_id: int) -> None:
        async with cls.session() as session:
            async with session.begin():
                rule = await session.get(RuleModel, rule_id)
                await session.delete(rule)

    @classmethod
    async def find_matching_rules(cls, rule: str) -> List[Rule]:
        """
        Find all rules that match this current rule
        """
        rules = []
        async with cls.session() as session:
            stmnt = select(RuleModel).where(RuleModel.rule == rule)
            results = await session.scalars(stmnt)
            for rule_item in results.all():
                rules.append(Rule.model_validate(rule_item))

        return rules
