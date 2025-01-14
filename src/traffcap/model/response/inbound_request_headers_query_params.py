from traffcap.model import (
    InboundRequestPublic,
    InboundRequestHeaderPublic,
    InboundRequestQueryParamPublic
)


class InboundRequestHeadersQueryParams(InboundRequestPublic, table=False):
    query_params: list[InboundRequestQueryParamPublic] = []
    headers: list[InboundRequestHeaderPublic] = []
