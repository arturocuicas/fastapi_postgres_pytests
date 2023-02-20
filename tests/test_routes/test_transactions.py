from uuid import UUID

import pytest
from fastapi import status

from db.repositories.transactions import TransactionRepository


@pytest.mark.asyncio
async def test_get_transactions(async_client):
    response = await async_client.get("/api/transactions/transactions")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_create_transaction(async_client, create_transaction):
    transaction = create_transaction()
    response = await async_client.post(
        "/api/transactions/transactions", json=transaction.dict()
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["amount"] == transaction.amount
    assert response.json()["description"] == transaction.description
    assert UUID(response.json()["id"])


@pytest.mark.asyncio
async def test_get_transaction(async_client, create_transaction):
    transaction = create_transaction()
    response_create = await async_client.post(
        "/api/transactions/transactions", json=transaction.dict()
    )
    response = await async_client.get(
        f"/api/transactions/transactions/{response_create.json()['id']}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == transaction.amount
    assert response.json()["description"] == transaction.description
    assert response.json()["id"] == response_create.json()["id"]


@pytest.mark.asyncio
async def test_delete_transaction(async_client, create_transaction):
    transaction = create_transaction()
    response_create = await async_client.post(
        "/api/transactions/transactions", json=transaction.dict()
    )
    response = await async_client.delete(
        f"/api/transactions/transactions/{response_create.json()['id']}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_update_transaction(async_client, create_transaction):
    transaction = create_transaction(amount=10, description="Init Description")
    response_create = await async_client.post(
        "/api/transactions/transactions", json=transaction.dict()
    )

    new_amount = 20
    new_description = "New Description"
    response = await async_client.put(
        f"/api/transactions/transactions/{response_create.json()['id']}",
        json={"amount": new_amount, "description": new_description},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == new_amount
    assert response.json()["description"] == new_description
    assert response.json()["id"] == response_create.json()["id"]


@pytest.mark.asyncio
async def test_get_transaction_paginated(db_session, async_client, create_transactions):
    repository = TransactionRepository(db_session)
    for transaction in create_transactions(_qty=4):
        await repository.create(transaction)

    response_page_1 = await async_client.get("/api/transactions/transactions?limit=2")
    assert len(response_page_1.json()) == 2

    response_page_2 = await async_client.get(
        "/api/transactions/transactions?limit=2&offset=2"
    )
    assert len(response_page_2.json()) == 2

    response = await async_client.get("/api/transactions/transactions")
    assert len(response.json()) == 4
