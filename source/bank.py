from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime


Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column("account_id", Integer, primary_key=True)
    balance = Column("balance", Float)
    transactions = relationship("Transaction", back_populates="accounts")  # Relation avec les emprunts

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def create_account(self):
        pass

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            transaction = Transaction(amount=amount, type="deposit", account_id=self)
            return transaction
        else:
            raise ValueError


    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                transaction = Transaction(amount=amount, type="withdrawal", account_id=self)
                return transaction
            else:
                raise ValueError
        else:
            raise ValueError

    def transfer(self, other_account, amount):
        if self.withdraw(amount):
            other_account.deposit(amount)
            return True
        else:
            return False
        
    def __repr__(self):
        return f"account_id={self.account_id}, balance='{self.balance}'"

    # def create_account(account_id, balance):
    #     # new_account = Account(account_id=account_id, balance=balance)

    # def get_balance(balance):
    #     return Account(balance=balance)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column("transaction_id", Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    amount = Column("amount", Float)
    type = Column("type", String)
    timestamp = Column("timestamp", DateTime, default=datetime.now)
    accounts = relationship("Account", back_populates="transactions")  # Relation avec les emprunts

    def __init__(self, amount, type, account_id):
        # super().__init__(account_id, balance)
        # self.transaction_id = transaction_id
        self.amount = amount
        self.type = type
        self.account_id = account_id


