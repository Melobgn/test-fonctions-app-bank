from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime

from bank import Account, Base, Transaction

def main():
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
    account.deposit()
    a2.withdraw()
    session.commit()



