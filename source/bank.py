from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column("account_id", Integer, primary_key=True)
    balance = Column("balance", Float)
    transactions = relationship("Transaction", back_populates="accounts")  # Relation avec les emprunts

    def __init__(self, account_id, balance, session):
        self.account_id = account_id
        self.balance = balance
        self.session = session


    def create_account(self):
        self.session.add(self)
        self.session.commit()


    def create_transaction(self, amount, type):
        transaction = Transaction(amount=amount, type=type, timestamp=datetime.now(), account_id=self.account_id)
        return transaction
        

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            new_transaction = self.create_transaction(amount=amount, type="deposit")
            self.session.add(new_transaction)
            self.session.commit()
        else:
            raise ValueError()


    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                new_transaction = self.create_transaction(amount=amount, type="withdraw")
                self.session.add(new_transaction)
                self.session.commit()
            else:
                raise ValueError()
        else:
            raise ValueError()

    def transfer(self, other_account, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            other_account.balance += amount
            transfer = self.create_transaction(amount, "transfer")
            self.session.add(transfer)
            self.session.commit()
        else:
            raise ValueError()
        
    def __repr__(self):
        return f"account_id={self.account_id}, balance='{self.balance}'"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column("transaction_id", Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    amount = Column("amount", Float)
    type = Column("type", String)
    timestamp = Column("timestamp", DateTime, default=datetime.now)
    accounts = relationship("Account", back_populates="transactions")  # Relation avec les emprunts

    # def __init__(self, amount, type, account_id):
    #     # super().__init__(account_id, balance)
    #     # self.transaction_id = transaction_id
    #     self.amount = amount
    #     self.type = type
    #     self.account_id = account_id


