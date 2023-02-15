from uuid import UUID, uuid4
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from db.repositories.transactions import TransactionRepository
from db.errors import EntityDoesNotExist
from schemas.transactions import TransactionPatch


@pytest.mark.asyncio
async def test_create_transaction(
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
async def test_get_transactions(
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


@pytest.mark.asyncio
async def test_get_transaction_by_id(
    db_session: AsyncSession,
    create_transaction
):
    transaction = create_transaction()
    repository = TransactionRepository(db_session)

    transaction_created = await repository.create(transaction)
    transaction_db = await repository.get(transaction_id=transaction_created.id)

    assert transaction_created == transaction_db


@pytest.mark.asyncio
async def test_get_transaction_by_id_not_found(
    db_session: AsyncSession
):
    repository = TransactionRepository(db_session)

    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(transaction_id=uuid4())


@pytest.mark.asyncio
async def test_update_transaction(
    db_session: AsyncSession,
    create_transaction
):
    init_amount = 10
    init_description = "Initial Description"
    final_amount = 20
    final_description = "Final Description"
    transaction = create_transaction(amount=init_amount, description=init_description)
    repository = TransactionRepository(db_session)
    db_transaction = await repository.create(transaction)

    update_transaction = await repository.patch(
        transaction_id=db_transaction.id,
        transaction_patch=TransactionPatch(
            amount=final_amount,
            description=final_description
        )
    )

    assert update_transaction.id == db_transaction.id
    assert update_transaction.amount == final_amount
    assert update_transaction.description == final_description


@pytest.mark.asyncio
async def test_soft_delete_transaction(
    db_session: AsyncSession,
    create_transaction
):
    transaction = create_transaction()
    repository = TransactionRepository(db_session)
    db_transaction = await repository.create(transaction)

    delete_transaction = await repository.delete(transaction_id=db_transaction.id)

    assert delete_transaction is None
    with pytest.raises(expected_exception=EntityDoesNotExist):
        await repository.get(transaction_id=db_transaction.id)

