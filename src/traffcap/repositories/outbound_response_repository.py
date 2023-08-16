from .repository import Repository
from traffcap.dto import Rule
from traffcap.model import OutboundResponseModel
from sqlalchemy import select
from typing import List


class OutboundResponseRepository(Repository):
    @classmethod
    async def get_by_rule_and_content_type(
        cls,
        rule: Rule,
        content_type: str
    ) -> List[Rule]:
        """
        Find all responses for this rule
        """
        responses = []
        async with cls.session() as session:
            results = await session.scalars(
                select(OutboundResponseModel)
                    .where(OutboundResponseModel.rule_id == rule.id)
                    .where(OutboundResponseModel.content_type == content_type)
            )
            for response in results.all():
                responses.append(Rule.model_validate(response))

        return responses
