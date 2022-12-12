import re
import uuid
import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr

camelcase_re = re.compile(r"([A-Z]+)(?=[a-z0-9])")


def camel_to_snake_case(name):
    def _join(match):
        word = match.group()

        if len(word) > 1:
            return ("_%s_%s" % (word[:-1], word[-1])).lower()

        return "_" + word.lower()

    return camelcase_re.sub(_join, name).lstrip("_")


@as_declarative()
class Base:
    __name__: str
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=datetime.datetime.now(),
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake_case(cls.__name__)
