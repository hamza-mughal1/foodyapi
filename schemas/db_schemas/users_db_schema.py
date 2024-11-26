from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Users Table
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    orders = relationship("Orders", back_populates="user", cascade="all, delete-orphan")