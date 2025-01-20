from enum import Enum


class HTTPVerbs(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    TRACE = "TRACE"

    @classmethod
    def to_list(cls):
        return [el.value for el in cls]
