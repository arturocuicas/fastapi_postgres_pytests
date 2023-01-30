from typing import Optional
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.errors import EntityDoesNotExist
from db.tables.transactions import Transaction
from schemas.transactions import TransactionCreate, TransactionRead


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, transaction_create: TransactionCreate) -> TransactionRead:
        db_transaction = Transaction.from_orm(transaction_create)
        self.session.add(db_transaction)
        await self.session.commit()
        await self.session.refresh(db_transaction)

        return TransactionRead(
            amount=db_transaction.amount, description=db_transaction.description
        )

    async def list(self) -> list[TransactionRead]:
        results = await self.session.execute(select(Transaction))

        return [
            TransactionRead(
                amount=transaction.amount, description=transaction.description
            )
            for transaction in results.scalars()
        ]

    async def get(self, transaction_id: UUID) -> Optional[TransactionRead]:
        transaction = await self.session.get(Transaction, transaction_id)

        if transaction is None:
            raise EntityDoesNotExist

        return TransactionRead(
            amount=transaction.amount, description=transaction.description
        )

    async def delete(self, transaction_id: UUID) -> None:
        transaction = await self.session.get(Transaction, transaction_id)

        if transaction is None:
            raise EntityDoesNotExist

        return await self.session.delete(transaction)
