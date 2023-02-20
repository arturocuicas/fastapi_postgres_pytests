import pytest
from pydantic import ValidationError

from schemas.transactions import TransactionCreate


def test_transaction_instance_empty():
    with pytest.raises(expected_exception=ValidationError):
        TransactionCreate()


def test_transaction_instance_amount_empty():
    with pytest.raises(expected_exception=ValidationError):
        TransactionCreate(description="Description")


def test_transaction_instance_description_empty():
    with pytest.raises(expected_exception=ValidationError):
        TransactionCreate(amount=10)


def test_transaction_instance_amount_wrong():
    with pytest.raises(expected_exception=ValidationError):
        TransactionCreate(amount="amount", description="Description")
