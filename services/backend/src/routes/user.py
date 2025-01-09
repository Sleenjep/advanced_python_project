from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Union

from src.database.db_init import get_db
from src.database.db_models import User, Order, OrderProduct, Product

router = APIRouter()

class ProductInOrder(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int

class OrderHistory(BaseModel):
    order_id: int
    order_date: Optional[datetime]
    products: List[ProductInOrder]

class UserPurchaseHistory(BaseModel):
    user_id: int
    username: str
    purchase_history: List[OrderHistory]

class NoPurchaseHistoryMessage(BaseModel):
    message: str

PurchaseHistoryResponse = Union[UserPurchaseHistory, NoPurchaseHistoryMessage]

@router.get("/purchase_history_{user_id}", response_model=PurchaseHistoryResponse)
async def get_purchase_history(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result_user = await db.execute(select(User).where(User.id == user_id))
    user = result_user.scalars().first()

    if not user:
        return {"error": "User not found"}

    result_orders = await db.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .options(selectinload(Order.order_products).selectinload(OrderProduct.product))
    )
    orders = result_orders.scalars().all()

    if not orders:
        return NoPurchaseHistoryMessage(message="No purchase history")

    purchase_history = []
    for order in orders:
        order_date = getattr(order, 'order_date', None)

        products_in_order = []
        for op in order.order_products:
            product = op.product
            if product:
                products_in_order.append(
                    ProductInOrder(
                        product_id=product.id,
                        name=product.name,
                        price=product.price,
                        quantity=op.quantity
                    )
                )

        purchase_history.append(
            OrderHistory(
                order_id=order.id,
                order_date=order_date,
                products=products_in_order
            )
        )

    return UserPurchaseHistory(
        user_id=user.id,
        username=user.username,
        purchase_history=purchase_history
    )

@router.get("/get_all_users")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return {"users": users}