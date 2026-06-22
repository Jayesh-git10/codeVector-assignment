from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String, Float, DateTime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)