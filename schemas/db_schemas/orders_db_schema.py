from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Orders Table
class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="orders", cascade="all, delete-orphan")