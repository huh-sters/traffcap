from .repository import Repository
from traffcap.dto import Rule
from traffcap.model import OutboundResponse
from sqlalchemy import select, ScalarResult


class OutboundResponseRepository(Repository):
    @classmethod
    async def get_by_rule_and_content_type(
        cls,
        rule: Rule,
        content_type: str
    ) -> ScalarResult[OutboundResponse]:
        """
        Find all responses for this rule
        """
        session = await cls.new_session()
        stmnt = (
            select(OutboundResponse)
                .where(OutboundResponse.rule_id == rule.id)
                .where(OutboundResponse.content_type == content_type)
        )
        return await session.scalars(stmnt)
