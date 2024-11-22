from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Orders Table
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")