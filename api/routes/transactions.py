from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from api.dependencies.repositories import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.transactions import TransactionRepository
from schemas.transactions import TransactionCreate, TransactionPatch, TransactionRead

router = APIRouter()


@router.post(
    "/transactions",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
    name="create_transaction",
)
async def create_transaction(
    transaction_create: TransactionCreate = Body(...),
    repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionRead:
    return await repository.create(transaction_create=transaction_create)


@router.get(
    "/transactions",
    response_model=list[Optional[TransactionRead]],
    status_code=status.HTTP_200_OK,
    name="get_transactions",
)
async def get_transactions(
    limit: int = Query(default=10, lte=100),
    offset: int = Query(default=0),
    repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> list[Optional[TransactionRead]]:
    return await repository.list(limit=limit, offset=offset)


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionRead,
    status_code=status.HTTP_200_OK,
    name="get_transaction",
)
async def get_transaction(
    transaction_id: UUID,
    repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionRead:
    try:
        await repository.get(transaction_id=transaction_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!"
        )

    return await repository.get(transaction_id=transaction_id)


@router.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_transaction",
)
async def delete_transaction(
    transaction_id: UUID,
    repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> None:
    try:
        await repository.get(transaction_id=transaction_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!"
        )

    return await repository.delete(transaction_id=transaction_id)


@router.put(
    "/transactions/{transaction_id}",
    response_model=TransactionRead,
    status_code=status.HTTP_200_OK,
    name="delete_transaction",
)
async def delete_transaction(
    transaction_id: UUID,
    transaction_patch: TransactionPatch = Body(...),
    repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> TransactionRead:
    try:
        await repository.get(transaction_id=transaction_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found!"
        )

    return await repository.patch(
        transaction_id=transaction_id, transaction_patch=transaction_patch
    )
