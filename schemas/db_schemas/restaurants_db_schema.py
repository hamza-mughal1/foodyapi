from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Orders Table
class Restaurants(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="restaurants")
    foods = relationship("Foods", back_populates="restaurants", cascade="all, delete-orphan")
    orders = relationship("Orders", back_populates="restaurants", cascade="all, delete-orphan")