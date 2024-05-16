import pytest
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from mock_alchemy.mocking import AlchemyMagicMock
from source.bank import Account, Base, Transaction


#Tests pour les dépôts

def test_deposit_normal(session, account_factory):
    account = account_factory(1, 500, session=session)
    account.deposit(50)
    assert account.balance == 550
    session.query(Account).filter(account.balance == 550).all()
    assert account.session.commit.call_count == 1

def test_deposit_normal(session, account_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        account.deposit(-50)
        assert account.balance == 500
        assert account.session.commit.call_count == 0
        # assert account.session.query(Transaction).count() == 1


def test_deposit_zero_amount(account_factory, session):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        account.deposit(0)

#Tests pour les retraits

def test_withdraw_normal(account_factory, session):
    account = account_factory(1, 500, session=session)
    account.withdraw(50)
    transaction = account.session.query(Transaction).first()
    assert account.balance == 450
    assert transaction.type == "withdraw"
    assert account.session.commit.call_count == 1

def test_withdraw_insufficient_funds(account_factory, session):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        account.withdraw(550)
        transaction = account.session.query(Transaction).first()
        assert transaction.type == "ValueError"
        assert account.session.commit.call_count == 0
        

def test_withdraw_negative_amount(account_factory, session):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        account.withdraw(0)
        assert account.balance == 500

#Tests pour les transferts

def test_transfer_normal(account_factory, session):
    account = account_factory(1, 500, session=session)
    other_account = account_factory(2, 300, session=session)
    account.transfer(other_account, 50)
    transaction = account.session.query(Transaction).first()
    transaction2 = other_account.session.query(Transaction).first()
    assert account.balance == 450 and other_account.balance == 350
    # assert transaction.type == "withdraw" and transaction2.type == "deposit"
    assert account.session.commit.call_count == 1
    
def test_transfer_insufficient_funds(account_factory, session):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        other_account = account_factory(2, 300, session=session)
        account.transfer(other_account, 550)
        transaction = account.session.query(Transaction).first()
        transaction2 = other_account.session.query(Transaction).first()
        assert account.balance == 500 and other_account.balance == 300
        assert transaction.type == "withdraw" and transaction2.type == "deposit"

#Tests pour la consultation de solde 

def test_get_balance_initial(account_factory, session):
    account = account_factory(1, 500, session=session)
    assert account.balance == 500
    account2 = account_factory(2, 300, session=session)
    balance = account2.get_balance()
    assert account2.balance == balance

def test_get_balance_after_deposit(account_factory, session):
    account = account_factory(1, 500, session=session)
    assert account.balance == 500
    account.deposit(50)
    balance = account.get_balance()
    assert balance == 550

def test_get_balance_after_withdrawal(account_factory, session):
    account = account_factory(1, 500, session=session)
    assert account.balance == 500
    account.withdraw(50)
    balance = account.get_balance()
    assert balance == 450

def test_get_balance_after_failed_withdrawal(account_factory, session):
    with pytest.raises(ValueError):
        account = account_factory(1, 500, session=session)
        assert account.balance == 500
        account.withdraw(550)
        balance = account.get_balance()
        assert balance == 500
        assert balance == account.balance

def test_get_balance_after_transfer(account_factory, session):
    account = account_factory(1, 500, session=session)
    other_account = account_factory(2, 300, session=session)
    account.transfer(other_account, 50)
    transfer1 = account.get_balance()
    transfer2 = other_account.get_balance()
    assert transfer1 == 450 and transfer2 == 350
    assert account.balance == 450 and other_account.balance == 350
    