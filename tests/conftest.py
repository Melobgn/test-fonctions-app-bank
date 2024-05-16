import pytest

from source.bank import Account, Transaction

from mock_alchemy.mocking import UnifiedAlchemyMagicMock

@pytest.fixture(scope="function")
def session():
    # Créez une mock session utilisant UnifiedAlchemyMagicMock
    session = UnifiedAlchemyMagicMock()
    yield session
    session.rollback()

@pytest.fixture
def account_factory():
    def new_account(account_id, balance, session):
        return Account(account_id=account_id, balance=balance, session=session)
    return new_account

