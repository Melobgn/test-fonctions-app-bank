from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from datetime import datetime
from init_db import *
from bank import Account, Base, Transaction

def main():
    db = init_db()
    Session = sessionmaker(bind=db.engine)
    session = Session()
    account = Account(1, 100, session)
    session.add(account)
    session.commit()

    a2 = Account(2, 50, session)
    session.add(a2)
    session.commit()

    # t1 = Transaction(200, "deposit", account.account_id)
    # t2 = Transaction(50, "withdrawal", a2.account_id)

    # session.add(t1)
    # session.add(t2)
    account.deposit(200)
    a2.withdraw(50)
    account.transfer(a2, 50)
    session.commit()

if __name__ == "__main__":
    main()



