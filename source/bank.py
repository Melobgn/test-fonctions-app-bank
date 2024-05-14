from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime
import init_db as init

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column("account_id", Integer, primary_key=True)
    balance = Column("balance", Float)
    transactions = relationship("Transaction", back_populates="accounts")  # Relation avec les emprunts

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        type = "deposit"
        transaction = Transaction(self.account_id, amount, type)
        return transaction


    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            type = "withdrawal"
            transaction = Transaction(self.account_id, amount, type)
            return transaction
        else:
            raise ValueError

    def transfer():
        pass

    def __repr__(self):
        return f"account_id={self.account_id}, balance='{self.balance}')"

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

    def __init__(self, transaction_id, amount, type, account_id):
        # super().__init__(account_id, balance)
        self.transaction_id = transaction_id
        self.amount = amount
        self.type = type
        self.account_id = account_id


engine = create_engine("sqlite:///bank.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
account = Account(1, 100)
session.add(account)
session.commit()

a2 = Account(2, 50)
session.add(a2)
session.commit()

t1 = Transaction(1, 200, "deposit", account.account_id)
t2 = Transaction(2, 50, "withdrawal", a2.account_id)

session.add(t1)
session.add(t2)
account.deposit(200)
a2.withdraw(50)
session.commit()