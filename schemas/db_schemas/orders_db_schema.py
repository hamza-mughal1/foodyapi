from sqlalchemy import Column, Enum, ForeignKey, Integer, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
from schemas.db_schemas import db_enums

# Orders Table
class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    order_status = Column(Enum(db_enums.OrderStatus), nullable=False, server_default=db_enums.OrderStatus.in_progress.value)
    acceptance_status = Column(Enum(db_enums.AcceptanceStatus), nullable=False, server_default=db_enums.AcceptanceStatus.pending.value)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="orders", cascade="all, delete-orphan")