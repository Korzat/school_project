from sqlalchemy import Column, BigInteger, Integer
from app.db.base_model import Base



class User(Base):
    __tablename__ = "users"
    tg_id = Column(BigInteger, primary_key=True)
    points = Column(Integer, default=0)

