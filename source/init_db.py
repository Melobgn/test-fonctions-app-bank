from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Float, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///bank.db", echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
