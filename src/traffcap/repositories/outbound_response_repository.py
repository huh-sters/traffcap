from .repository import Repository
from traffcap.dto import Rule, OutboundResponse
from traffcap.model import OutboundResponseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List


class OutboundResponseRepository(Repository):
    @classmethod
    async def get_by_rule_and_content_type(
        cls,
        rule: Rule,
        content_type: str
    ) -> List[OutboundResponse]:
        """
        Find all responses for this rule
        """
        responses = []
        async with cls.session() as session:
            results = await session.scalars(
                select(OutboundResponseModel)
                    .where(OutboundResponseModel.rule_id == rule.id)
                    .where(OutboundResponseModel.content_type == content_type)
                    .options(selectinload(OutboundResponseModel.rule))
            )
            for response in results.all():
                responses.append(OutboundResponse.model_validate(response))

        return responses
