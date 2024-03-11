import uuid as uuid_pkg
from datetime import datetime

from sqlmodel import Field, SQLModel, text


class UUIDModel(SQLModel):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={
            # "server_default": text("gen_random_uuid()"),
            "unique": True,
        },
    )


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp")},
    )

    updated_at: datetime = Field(
        nullable=True,
        sa_column_kwargs={
            "onupdate": text("current_timestamp"),
        },
    )


class SoftDeleteModel(SQLModel):
    deleted_at: datetime = Field(nullable=True)
