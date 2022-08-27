from sqlalchemy import Column, Integer, String, Float

from database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    brand = Column(String)
