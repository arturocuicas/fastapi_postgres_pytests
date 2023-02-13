from uuid import UUID
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession


from db.repositories.transactions import TransactionRepository


@pytest.mark.asyncio
async def test_transaction_create(
    db_session: AsyncSession,
    create_transaction
):
    transaction = create_transaction()
    repository = TransactionRepository(db_session)
    db_transaction = await repository.create(transaction)

    assert db_transaction.amount == transaction.amount
    assert db_transaction.description == transaction.description
    assert isinstance(db_transaction.id, UUID)


@pytest.mark.asyncio
async def test_transactions_get(
    db_session: AsyncSession,
    create_transaction
):
    transaction = create_transaction()
    repository = TransactionRepository(db_session)
    await repository.create(transaction)

    db_transactions = await repository.list()

    assert isinstance(db_transactions, list)
    assert db_transactions[0].amount == transaction.amount
    assert db_transactions[0].description == transaction.description
