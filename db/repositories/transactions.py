from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.tables.base_class import StatusEnum
from db.tables.transactions import Transaction
from schemas.transactions import TransactionCreate, TransactionPatch, TransactionRead


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, transaction_id: UUID):
        statement = (
            select(Transaction)
            .where(Transaction.id == transaction_id)
            .where(Transaction.status != StatusEnum.deleted)
        )
        results = await self.session.exec(statement)

        return results.first()

    async def create(self, transaction_create: TransactionCreate) -> TransactionRead:
        db_transaction = Transaction.from_orm(transaction_create)
        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)

        return TransactionRead(**db_transaction.dict())

    async def list(self, limit: int = 10, offset: int = 0) -> list[TransactionRead]:
        statement = (
            (select(Transaction).where(Transaction.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        results = await self.session.exec(statement)

        return [TransactionRead(**transaction.dict()) for transaction in results]

    async def get(self, transaction_id: UUID) -> Optional[TransactionRead]:
        db_transaction = await self._get_instance(transaction_id)

        if db_transaction is None:
            raise EntityDoesNotExist

        return TransactionRead(**db_transaction.dict())

    async def patch(
        self, transaction_id: UUID, transaction_patch: TransactionPatch
    ) -> Optional[TransactionRead]:
        db_transaction = await self._get_instance(transaction_id)

        if db_transaction is None:
            raise EntityDoesNotExist

        transaction_data = transaction_patch.dict(exclude_unset=True, exclude={"id"})
        for key, value in transaction_data.items():
            setattr(db_transaction, key, value)

        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)

        return TransactionRead(**db_transaction.dict())

    async def delete(self, transaction_id: UUID) -> None:
        db_transaction = await self._get_instance(transaction_id)

        if db_transaction is None:
            raise EntityDoesNotExist

        setattr(db_transaction, "status", StatusEnum.deleted)
        self.session.add(db_transaction)

        await self.session.commit()
