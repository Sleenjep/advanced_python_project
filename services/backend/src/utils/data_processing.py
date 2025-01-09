import pandas as pd
from typing import List

from src.database.db_models import Order, OrderProduct, Product

def orders_to_df(orders_list: List[Order]) -> pd.DataFrame:
    data = [
        [
            o.id,
            o.user_id,
            o.eval_set,
            o.order_number,
            o.order_dow,
            o.order_hour_of_day,
            o.days_since_prior_order,
        ]
        for o in orders_list
    ]
    return pd.DataFrame(
        data,
        columns=[
            "order_id",
            "user_id",
            "eval_set",
            "order_number",
            "order_dow",
            "order_hour_of_day",
            "days_since_prior_order",
        ],
    )

def orderproducts_to_df(op_list: List[OrderProduct]) -> pd.DataFrame:
    data = [
        [op.order_id, op.product_id, op.add_to_cart_order, op.reordered]
        for op in op_list
    ]
    return pd.DataFrame(
        data,
        columns=["order_id", "product_id", "add_to_cart_order", "reordered"]
    )

def products_to_df(prod_list: List[Product]) -> pd.DataFrame:
    data = [
        [p.id, p.aisle_id, p.department_id]
        for p in prod_list
    ]
    return pd.DataFrame(
        data,
        columns=["product_id", "aisle_id", "department_id"]
    )

def extend_priors(priors: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    orders_indexed = orders.set_index("order_id")[["order_number", "user_id"]]
    priors = priors.join(orders_indexed, on="order_id")
    return priors