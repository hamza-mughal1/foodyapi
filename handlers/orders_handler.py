from fastapi import APIRouter, HTTPException
from schemas.pydantic_schemas import orders_pydantic_schema as order_schema
from models.orders_model import OrderModel
from utilities.dependencies import db_dependency, token_dependency
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

order = OrderModel()


@router.post("/")
async def create_order(order_data: List[order_schema.OrderItem], db: db_dependency, token: token_dependency):
    if order_data == []:
        raise HTTPException(status_code=422, detail="No data was passed")
    return await order.create_order(order_data, db, token)
