import pytest
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from mock_alchemy.mocking import AlchemyMagicMock
from source.bank import Account, Base, Transaction


#Tests pour les dépôts

def test_deposit_normal(account_factory, transaction_factory):
    session = AlchemyMagicMock()
    account = account_factory(1, 500)
    session.add(account)
    session.commit()
    transaction = transaction_factory(50, "deposit", account.account_id)
    session.add(transaction)
    account.deposit(50)
    session.commit()
    assert account.balance == 550
    session.query(Account).filter(account.balance == 550).all()
    session.query(Transaction).filter(transaction.type == "deposit")

# def test_deposit_negative_amount(account_factory, transaction_factory):
#     session = AlchemyMagicMock()
#     with pytest.raises(ValueError):
#         account = account_factory(1, 500)
#         session.add(account)
#         session.commit()
#         transaction = transaction_factory(-50, "deposit", account.account_id)
#         session.add(transaction)
#         account.deposit(-50)
#         session.commit()
#         assert account.balance == 500
#         assert transaction.type == "deposit"
#         session.query(Account).filter(account.balance == 500).all()
#         session.query(Transaction).filter(transaction.type == "deposit")

def test_deposit_zero_amount(account_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500)
        account.deposit(0)

#Tests pour les retraits

def test_withdraw_normal(account_factory, transaction_factory):
    account = account_factory(1, 500)
    transaction = transaction_factory(50, "withdraw", account.account_id)
    account.withdraw(50)
    assert account.balance == 450
    assert transaction.type == "withdraw"


def test_withdraw_insufficient_funds(account_factory, transaction_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500)
        transaction = transaction_factory(550, "withdraw", account.account_id)
        account.withdraw(550)
        assert transaction.type == "ValueError"
        

def test_withdraw_negative_amount(account_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500)
        account.withdraw(0)
        assert account.balance == 500

#Tests pour les transferts

def test_transfer_normal(account_factory, transaction_factory):
    account = account_factory(1, 500)
    other_account = account_factory(2, 300)
    transaction = transaction_factory(50, "withdraw", account.account_id)
    account.transfer(other_account, 50)
    transaction2 = transaction_factory(50, "deposit", other_account.account_id)
    assert account.balance == 450 and other_account.balance == 350
    assert transaction.type == "withdraw" and transaction2.type == "deposit"
    
def test_transfer_insufficient_funds(account_factory, transaction_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500)
        other_account = account_factory(2, 300)
        transaction = transaction_factory(550, "withdraw", account.account_id)
        account.transfer(other_account, 550)
        transaction2 = transaction_factory(550, "deposit", other_account.account_id)
        assert account.balance == 500 and other_account.balance == 300
        assert transaction.type == "withdraw" and transaction2.type == "deposit"

#Tests pour la consultation de solde 

def test_get_balance_initial(account_factory):
    account = account_factory(1, 500)
    assert account.balance == 500
    account2 = account_factory(2, 300)
    balance = account2.get_balance()
    assert account2.balance == balance

def test_get_balance_after_deposit(account_factory):
    account = account_factory(1, 500)
    assert account.balance == 500
    account.deposit(50)
    balance = account.get_balance()
    assert balance == 550

def test_get_balance_after_withdrawal(account_factory):
    account = account_factory(1, 500)
    assert account.balance == 500
    account.withdraw(50)
    balance = account.get_balance()
    assert balance == 450

def test_get_balance_after_failed_withdrawal(account_factory):
    with pytest.raises(ValueError):
        account = account_factory(1, 500)
        assert account.balance == 500
        account.withdraw(550)
        balance = account.get_balance()
        assert balance == 500
        assert balance == account.balance

def test_get_balance_after_transfer(account_factory, transaction_factory):
    account = account_factory(1, 500)
    other_account = account_factory(2, 300)
    account.transfer(other_account, 50)
    transfer1 = account.get_balance()
    transfer2 = other_account.get_balance()
    assert transfer1 == 450 and transfer2 == 350
    assert account.balance == 450 and other_account.balance == 350
    
