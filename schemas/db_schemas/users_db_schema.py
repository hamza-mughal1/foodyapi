from sqlalchemy import Column, Enum, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base
from schemas.db_schemas import db_enums

# Users Table
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    user_role = Column(Enum(db_enums.UserRole), nullable=False, server_default=db_enums.UserRole.user.value)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    orders = relationship("Orders", back_populates="users", cascade="all, delete-orphan")
    restaurants = relationship("Restaurants", back_populates="users", cascade="all, delete-orphan")
    access_tokens = relationship("AccessTokens", back_populates="users", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshTokens", back_populates="users", cascade="all, delete-orphan")