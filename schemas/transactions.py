from db.tables.base_class import UUIDModel
from db.tables.transactions import TransactionBase


class TransactionCreate(TransactionBase):
    ...


class TransactionRead(UUIDModel, TransactionBase):
    ...
