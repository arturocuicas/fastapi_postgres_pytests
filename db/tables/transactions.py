from sqlmodel import Field, SQLModel

from db.tables.base_class import TimestampModel, UUIDModel, StatusEnum


class TransactionBase(SQLModel):
    amount: int = Field(nullable=False)
    description: str = Field(nullable=False)


class Transaction(TransactionBase, UUIDModel, TimestampModel, table=True):
    status: StatusEnum = Field(default=StatusEnum.inactive)

    __tablename__ = "transactions"
