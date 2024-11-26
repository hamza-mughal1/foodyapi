from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base


# Foods Table
class Foods(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    order_items = relationship("OrderItems", back_populates="food", cascade="all, delete-orphan")
