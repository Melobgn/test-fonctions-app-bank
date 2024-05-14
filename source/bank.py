from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime
import init_db as init

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column("account_id", Integer, primary_key=True)
    balance = Column("balance", Float)
    accounts = relationship("Transaction", back_populates="transactions")  # Relation avec les emprunts


    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def __repr__(self):
        return f"Account(account_id={self.account_id}, balance='{self.balance}')"

    def create_account(account_id, balance):
        new_account = Account(account_id=account_id, balance=balance)

    def get_balance(balance):
        return Account(balance=balance)



class Transaction(Account):
    __tablename__ = "transactions"

    transaction_id = Column("transaction_id", Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    amount = Column("amount", Float)
    type = Column("type", String)
    timestamp = Column("timestamp", DateTime, default=datetime.now)
    transactions = relationship("Account", back_populates="accounts")  # Relation avec les emprunts

    def __init__(self, account_id, balance, transaction_id, amount, type, timestamp):
        super().__init__(account_id, balance)
        self.transaction_id = transaction_id
        self.amount = amount
        self.type = type
        self.timestamp = timestamp

    def deposit(balance, amount):
        return balance + amount

    def withdraw(balance, amount):
        withdrawal = balance - amount
        if balance < 0:
            raise ValueError
        else:
            return withdrawal

    def transfer():
        pass

    def __repr__(self):
        return f"Transaction(transaction_id={self.transaction_id}, amount='{self.amount}, type='{self.type}')"
    

engine = create_engine("sqlite:///bank.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = init.Session()
account = Account(1, 100)
session.add(account)
session.commit()

a2 = Account(2, 50)
session.add(a2)
session.commit()