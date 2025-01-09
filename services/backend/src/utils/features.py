import pandas as pd
import numpy as np

def get_product_features(priors: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    prods = pd.DataFrame()
    prods["orders"] = priors.groupby("product_id").size().astype(np.int32)
    prods["reorders"] = priors.groupby("product_id")["reordered"].sum().astype(np.float32)
    prods["reorder_rate"] = (prods["reorders"] / prods["orders"]).astype(np.float32)
    
    products = products.set_index("product_id")
    products = products.join(prods, on="product_id")
    products.reset_index(inplace=True)
    return products

def get_user_features(priors: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    usr = pd.DataFrame()
    usr["average_days_between_orders"] = orders.groupby("user_id")["days_since_prior_order"].mean().astype(np.float32)
    usr["nb_orders"] = orders.groupby("user_id").size().astype(np.int16)

    users = pd.DataFrame()
    users["total_items"] = priors.groupby("user_id").size().astype(np.int16)
    users["all_products"] = priors.groupby("user_id")["product_id"].apply(set)
    users["total_distinct_items"] = users["all_products"].map(len).astype(np.int16)

    users = users.join(usr)
    users["average_basket"] = (users["total_items"] / users["nb_orders"]).astype(np.float32)
    return users

def get_userXproduct_features(priors: pd.DataFrame) -> pd.DataFrame:
    priors["user_product"] = priors["product_id"] + priors["user_id"] * 100000
    d = {}
    for row in priors.itertuples():
        key = row.user_product
        if key not in d:
            d[key] = (1, (row.order_number, row.order_id), row.add_to_cart_order)
        else:
            old_val = d[key]
            new_count = old_val[0] + 1
            new_last = max(old_val[1], (row.order_number, row.order_id))
            new_pos_sum = old_val[2] + row.add_to_cart_order
            d[key] = (new_count, new_last, new_pos_sum)

    userXproduct = pd.DataFrame.from_dict(d, orient="index")
    userXproduct.columns = ["nb_orders", "last_order_tuple", "sum_pos_in_cart"]
    userXproduct["nb_orders"] = userXproduct["nb_orders"].astype(np.int16)
    userXproduct["last_order_id"] = userXproduct["last_order_tuple"].map(lambda x: x[1]).astype(np.int32)
    userXproduct["sum_pos_in_cart"] = userXproduct["sum_pos_in_cart"].astype(np.int16)
    userXproduct.drop("last_order_tuple", axis=1, inplace=True)
    return userXproduct

def get_all_features(
    df: pd.DataFrame,
    orders: pd.DataFrame,
    userXproduct: pd.DataFrame,
    users: pd.DataFrame,
    products: pd.DataFrame
):
    df["user_total_orders"] = df["user_id"].map(users["nb_orders"])
    df["user_total_items"] = df["user_id"].map(users["total_items"])
    df["total_distinct_items"] = df["user_id"].map(users["total_distinct_items"])
    df["user_average_days_between_orders"] = df["user_id"].map(users["average_days_between_orders"])
    df["user_average_basket"] = df["user_id"].map(users["average_basket"])

    df["aisle_id"] = df["product_id"].map(products["aisle_id"])
    df["department_id"] = df["product_id"].map(products["department_id"])
    df["product_orders"] = df["product_id"].map(products["orders"]).astype(np.float32)
    df["product_reorders"] = df["product_id"].map(products["reorders"])
    df["product_reorder_rate"] = df["product_id"].map(products["reorder_rate"])

    df["z"] = df["user_id"] * 100000 + df["product_id"]
    df["UP_orders"] = df["z"].map(userXproduct["nb_orders"])
    df["UP_orders_ratio"] = (df["UP_orders"] / df["user_total_orders"]).astype(np.float32)
    df["UP_average_pos_in_cart"] = (
        df["z"].map(userXproduct["sum_pos_in_cart"]) / df["UP_orders"]
    ).astype(np.float32)

    df["UP_last_order_id"] = df["z"].map(userXproduct["last_order_id"])
    order_id_to_number = orders.set_index("order_id")["order_number"].to_dict()
    df["UP_orders_since_last"] = df["user_total_orders"] - df["UP_last_order_id"].map(order_id_to_number)
    df["UP_reorder_rate"] = (df["UP_orders"] / df["user_total_orders"]).astype(np.float32)

    df.drop(["z", "UP_last_order_id"], axis=1, inplace=True)

    f_to_use = [
        "user_total_orders",
        "user_total_items",
        "total_distinct_items",
        "user_average_days_between_orders",
        "user_average_basket",
        "aisle_id",
        "department_id",
        "product_orders",
        "product_reorders",
        "product_reorder_rate",
        "UP_orders",
        "UP_orders_ratio",
        "UP_average_pos_in_cart",
        "UP_orders_since_last",
        "UP_reorder_rate",
    ]
    return df[f_to_use]

def select_pairs_for_user(user_id: int, products_df: pd.DataFrame, top_n: int = 1000) -> pd.DataFrame:
    products_sorted = products_df.dropna(subset=["reorder_rate"]).sort_values("reorder_rate", ascending=False)
    selected = products_sorted.head(top_n).index
    df_pairs = pd.DataFrame({"user_id": [user_id] * len(selected), "product_id": selected})
    return df_pairs