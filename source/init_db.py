from sqlalchemy import create_engine
from bank import Base

def init_db():
    engine = create_engine('sqlite:///bank.db')

    try:

        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        print(e)

    return engine

