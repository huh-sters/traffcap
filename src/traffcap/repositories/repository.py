from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
from traffcap.model import Base


class Repository:
    engine = None

    @classmethod
    @contextmanager
    def session(cls):
        cls.engine = create_engine("sqlite:///test.db", echo=True)
        yield Session(cls.engine)

    @classmethod
    def upgrade(cls) -> None:
        engine = create_engine("sqlite:///test.db", echo=True)
        Base.metadata.create_all(engine)
