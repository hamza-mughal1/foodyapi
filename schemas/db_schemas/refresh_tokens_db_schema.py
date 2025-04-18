from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base

# Users Table
class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token_id = Column(Integer, ForeignKey("access_tokens.id"), nullable=False)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    users = relationship("Users", back_populates="refresh_tokens")
    access_tokens = relationship("AccessTokens", back_populates="refresh_tokens")
