from typing import List
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .outbound_response import OutboundResponseModel
    from .rule_match import RuleMatchModel

"""
Rules are used by Traffcap to decide how to respond to an inbound request.

A rule is first matched against one of the aspects of the request:
1. Path match
2. Header match

If any of these rules match, then the rules response payload is prepared and sent.

Body matching is not being used at this time. To detect XML/JSON/CSV, use the content type header.

Path Match
==========

The incoming request will be something like:

https://url/r/<endpoint code>

The path matching rule is applied to the <endpoint code> part of the URL.

Why? Traffcap will accept traffic to any endpoint code and does not require the
setup of specific endpoint codes prior to accepting traffic. This means that any
application that wants to send messages does not need to setup any codes prior to
just sending the message. It can just send random endpoint codes and Traffcap will
record the data.

If a client wanted to receive specific responses to a call to a specific endpoint, it
can use the rule path matching for just this. For example:

Rule match: ^ABCDEF_.*$

This will match any endpoint code that starts with `ABCDEF_` and then send the correct response. It means that
an application can append random characters to the end of the endpoint code to identify messages for a particular
session. Like:

ABCDEF_DEADBEEF9876

Alternatively, an exact endpoint code can be matched by:

^ABCDEF$

Header match
============

Any header in the payload can match.

1. The existance of a matching header
2. The matching content of the value in a header

The process will iterate over all the headers in the payload and match the key first and then the value

Matches can be grouped logically, so with three matches A, B and C. We can say match A AND B, but not C.

Or A OR B OR C.


Matching
========

All matches are performed using Regex. This grants us the ability to still use exact matches. The UI can
be presented as either an exact match or a Regex match, but beneath the hood it just performs Regex matches.

The path match is a single Regex
The header matches are a collection of key and value Regexs

"""

class RuleModel(Base):
    __tablename__: str = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    matches: Mapped[List["RuleMatchModel"]] = relationship(
        back_populates="rules"
    )
    outbound_responses: Mapped[List["OutboundResponseModel"]] = relationship(  # noqa: F821
        back_populates="rules"
    )
