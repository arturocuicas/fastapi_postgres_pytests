from sqlmodel import SQLModel

from db.tables.base_class import TimestampModel, UUIDModel


class TransactionBase(SQLModel):
    amount: int
    description: str


class Transaction(TransactionBase, UUIDModel, TimestampModel, table=True):
    ...
