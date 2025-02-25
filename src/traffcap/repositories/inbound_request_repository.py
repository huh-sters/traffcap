import logging
from typing import Sequence
from .repository import Repository
from fastapi import Request
from traffcap.model import (
    InboundRequest,
    InboundRequestHeader,
    InboundRequestQueryParam
)
from sqlmodel import select, func, col


class InboundRequestRepository(Repository):
    @classmethod
    async def store_request(
        cls,
        endpoint_code: str,
        request: Request
    ) -> None:
        async with cls.session() as session:
            try:
                new_request = await InboundRequest.from_request(endpoint_code, request)
                for key in request.headers:
                    new_request.headers.append(
                        InboundRequestHeader(
                            key=key,
                            value=request.headers[key]
                        )
                    )
                for key in request.query_params:
                    new_request.query_params.append(
                        InboundRequestQueryParam(
                            key=key,
                            value=request.query_params[key]
                        )
                    )
                session.add(new_request)
                await session.commit()

            except Exception as ex:
                logging.info(ex)

    @classmethod
    async def get_all_inbound_requests(cls) -> Sequence[InboundRequest]:
        async with cls.session() as session:
            return (await session.exec(select(InboundRequest))).unique().all()

        return []

    @classmethod
    async def get_inbound_requests_by_page(cls, page_size: int = 20, page: int = 0) -> Sequence[InboundRequest]:
        async with cls.session() as session:
            return (await session.exec(select(InboundRequest).limit(page_size).offset(page))).unique().all()

        return []

    @classmethod
    async def get_inbound_request_count(cls) -> int:
        try:
            async with cls.session() as session:
                return (await session.exec(select(func.count(col(InboundRequest.id))))).one()
        except Exception as ex:
            logging.error(ex)
        return 0