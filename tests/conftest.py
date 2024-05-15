import pytest

from source.bank import Account, Transaction

@pytest.fixture
def account_factory():
    def new_account(account_id, balance):
        return Account(account_id=account_id, balance=balance)
    return new_account

@pytest.fixture
def transaction_factory():
    def new_transaction(amount, type, account_id):
        return Transaction(amount=amount, type=type, account_id=account_id)
    return new_transaction
