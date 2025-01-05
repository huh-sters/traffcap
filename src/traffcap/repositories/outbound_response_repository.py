from typing import Sequence
from .repository import Repository
from traffcap.model import Rule, OutboundResponse
from sqlmodel import select


class OutboundResponseRepository(Repository):
    @classmethod
    async def get_by_rule_and_content_type(
        cls,
        rule: Rule,
        content_type: str
    ) -> Sequence[OutboundResponse]:
        async with cls.session() as session:
            results = await session.scalars(
                select(OutboundResponse)
                    .where(OutboundResponse.rule_id == rule.id)
                    .where(OutboundResponse.content_type == content_type)
            )
            return results.all()

        return []
