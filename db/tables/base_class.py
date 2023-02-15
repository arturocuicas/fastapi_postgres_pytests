from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, text
from sqlmodel import Field, SQLModel


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"


class UUIDModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )
