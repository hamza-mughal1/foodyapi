from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Users Table
class AccessTokens(Base):
    __tablename__ = "access_tokens"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="access_tokens")
    refresh_tokens = relationship("RefreshTokens", back_populates="access_tokens", cascade="all, delete-orphan")