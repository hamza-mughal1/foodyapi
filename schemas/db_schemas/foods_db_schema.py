from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from engines.sql_engine import Base


# Foods Table
class Foods(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    order_items = relationship("OrderItems", back_populates="foods", cascade="all, delete-orphan")
    restaurants = relationship("Restaurants", back_populates="foods")
