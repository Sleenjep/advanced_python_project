from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.db_models import Order, OrderProduct, Product
from src.database.db_init import get_db

from src.utils.models import RecommendationModel
from src.utils.data_processing import (
    orders_to_df, orderproducts_to_df, products_to_df, extend_priors
)
from src.utils.features import (
    get_product_features, get_user_features, get_userXproduct_features,
    get_all_features, select_pairs_for_user
)

router = APIRouter()

rec_model = RecommendationModel(model_path="./src/baseline.txt")

@router.get("/user_{user_id}")
async def predict_recommendations(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result_orders = await db.execute(select(Order))
    orders_list = result_orders.scalars().all()
    df_orders = orders_to_df(orders_list)

    prior_orders_ids = df_orders[df_orders["eval_set"] == "prior"]["order_id"].unique().tolist()
    result_op_prior = await db.execute(
        select(OrderProduct).where(OrderProduct.order_id.in_(prior_orders_ids))
    )
    priors_list = result_op_prior.scalars().all()
    df_priors = orderproducts_to_df(priors_list)

    result_products = await db.execute(select(Product))
    products_list = result_products.scalars().all()
    df_products = products_to_df(products_list)

    df_priors = extend_priors(df_priors, df_orders)
    df_products = get_product_features(df_priors, df_products)
    df_products.set_index("product_id", inplace=True, drop=False)
    users_df = get_user_features(df_priors, df_orders)
    userXproduct_df = get_userXproduct_features(df_priors)

    df_pairs = select_pairs_for_user(user_id, df_products, top_n=1000)
    df_features = get_all_features(
        df_pairs.copy(),
        df_orders,
        userXproduct_df,
        users_df,
        df_products
    )

    preds = rec_model.predict(df_features)
    df_pairs["preds"] = preds
    df_pairs_sorted = df_pairs.sort_values("preds", ascending=False).head(10)

    recommended_products = df_pairs_sorted["product_id"].tolist()

    result_product_names = await db.execute(
        select(Product.id, Product.name).where(Product.id.in_(recommended_products))
    )
    product_names = {row.id: row.name for row in result_product_names}

    recommended_products_with_names = [
        {"product_id": product_id, "name": product_names.get(product_id, "Unknown")}
        for product_id in recommended_products
    ]

    return {
        "user_id": user_id,
        "recommended_products": recommended_products_with_names
    }