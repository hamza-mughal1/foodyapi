from sqlalchemy import Column, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Order Items Table
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity = Column(Integer, nullable=False, server_default="1")
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    order = relationship("Order", back_populates="order_items")
    food = relationship("Food", back_populates="order_items")
