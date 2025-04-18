from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.order_items_db_schema import OrderItems
from schemas.db_schemas.orders_db_schema import Orders
from schemas.db_schemas.foods_db_schema import Foods
from schemas.pydantic_schemas import orders_pydantic_schema as order_schema
from typing import List
from utilities.utils import check_if_vendor_has_a_restaurant
from fastapi import HTTPException, status

class OrderModel:
    def __init__(self):
        pass

    async def create_order(self, order_data: List[order_schema.OrderItem], db: AsyncSession, token: dict):
        total_price = 0
        user_id = token["user_id"]
        orders_list = []
        restaurant_id = None
        
        for i in order_data:
            order = i.model_dump()
            result = await db.execute(
            select(Foods).where(
                Foods.id == order["id"]
                )
            )
            food =  result.scalar_one_or_none()
            if restaurant_id is None:
                restaurant_id = food.restaurant_id
            else:
                if restaurant_id != food.restaurant_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="all foods must have same restaurant")
            
            price = food.price * order["quantity"]
            total_price += price
            orders_list.append((order["id"], order["quantity"], price))
            
        try:
            # Begin transaction
            orders = Orders(user_id=user_id, price=total_price, restaurant_id=restaurant_id)
            db.add(orders)

            # Flush to generate the `id` for `orders`
            await db.flush()
            order_id = orders.id

            # Add order items
            for i in orders_list:
                order_item = OrderItems(order_id=order_id, food_id=i[0], quantity=i[1], price=i[2])
                db.add(order_item)

            # Commit the transaction
            await db.commit()
        except Exception as e:
            # Roll back in case of an error
            await db.rollback()
            raise e  # Re-raise the exception for higher-level handling/logging

        return {"message": "order has been placed!"}

    async def pending_orders(self, db: AsyncSession, token: dict):
        restaurant = await check_if_vendor_has_a_restaurant(db, token)
        result = await db.execute(
            select(Orders).where(
                and_(
                    Orders.restaurant_id == restaurant.id,
                    Orders.acceptance_status == 'pending'
                )
            )
        )
        orders = result.scalars().all()
        
        return orders