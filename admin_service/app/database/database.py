from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messenger_shalaev'

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    receiver_name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
