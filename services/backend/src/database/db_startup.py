import csv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, insert
from passlib.context import CryptContext

from ..database.db_models import User, Product, Department, Aisle, Order, OrderProduct

PRODUCTS_PATH = "src/database/csvs/products.csv"
DEPARTMENTS_PATH = "src/database/csvs/departments.csv"
AISLES_PATH = "src/database/csvs/aisles.csv"
ORDERS_PATH = "src/database/csvs/orders.csv"
ORDER_PRODUCTS_PATH = "src/database/csvs/order_products__prior.csv" 
ORDER_PRODUCTS_TRAIN_PATH = "src/database/csvs/order_products__train.csv"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_default_user(db: AsyncSession):
    result = await db.execute(select(User).where(User.username == "admin"))
    user = result.scalars().first()

    if user is None:
        admin_user_id = 0
        hashed_password = pwd_context.hash("admin")
        new_user = User(id=admin_user_id, username="admin", hashed_password=hashed_password, is_admin=True)
        db.add(new_user)
        await db.commit()

async def create_users_from_orders(db: AsyncSession):
    user_ids = set()

    with open(ORDERS_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row.get('user_id')
            if user_id:
                try:
                    user_ids.add(int(user_id))
                except ValueError:
                    continue

    for user_id in user_ids:
        if user_id == 0:
            continue

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            username = f"user{user_id}"
            default_password = f"user{user_id}"
            hashed_password = pwd_context.hash(default_password)
            new_user = User(
                username=username,
                hashed_password=hashed_password,
                is_admin=False
            )
            db.add(new_user)

    await db.commit()

async def create_departments(db: AsyncSession):
    with open(DEPARTMENTS_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = await db.execute(select(Department).where(Department.id == int(row['department_id'])))
            department = result.scalars().first()

            if department is None:
                new_department = Department(
                    id=int(row['department_id']),
                    name=row['department']
                )
                db.add(new_department)

    await db.commit()

async def create_aisles(db: AsyncSession):
    with open(AISLES_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = await db.execute(select(Aisle).where(Aisle.id == int(row['aisle_id'])))
            aisle = result.scalars().first()

            if aisle is None:
                new_aisle = Aisle(
                    id=int(row['aisle_id']),
                    name=row['aisle']
                )
                db.add(new_aisle)

    await db.commit()

async def create_products(db: AsyncSession):
    with open(PRODUCTS_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if 'product_id' not in reader.fieldnames:
            raise ValueError(f"'product_id' column is missing in {PRODUCTS_PATH}")
        for row in reader:
            result = await db.execute(select(Product).where(Product.id == int(row['product_id'])))
            product = result.scalars().first()

            if product is None:
                new_product = Product(
                    id=int(row['product_id']),
                    name=row['product_name'],
                    price=float(row['product_price']),
                    department_id=int(row['department_id']),
                    aisle_id=int(row['aisle_id'])
                )
                db.add(new_product)

    await db.commit()

async def create_orders(db: AsyncSession):
    with open(ORDERS_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result = await db.execute(select(Order).where(Order.id == int(row['order_id'])))
            order = result.scalars().first()

            if order is None:
                days_since_prior_order = row['days_since_prior_order'].strip()
                days_since_prior_order = float(days_since_prior_order) if days_since_prior_order else None

                new_order = Order(
                    id=int(row['order_id']),
                    user_id=int(row['user_id']),
                    eval_set=row['eval_set'],
                    order_number=int(row['order_number']),
                    order_dow=int(row['order_dow']),
                    order_hour_of_day=int(row['order_hour_of_day']),
                    days_since_prior_order=days_since_prior_order
                )
                db.add(new_order)

    await db.commit()

async def create_order_products(db: AsyncSession):
    for path in [ORDER_PRODUCTS_PATH, ORDER_PRODUCTS_TRAIN_PATH]:
        with open(path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                result = await db.execute(select(OrderProduct).where(
                    and_(
                        OrderProduct.order_id == int(row['order_id']),
                        OrderProduct.product_id == int(row['product_id'])
                    )
                ))
                order_product = result.scalars().first()

                if order_product is None:
                    reordered = row['reordered']
                    reordered = bool(int(reordered)) if reordered else False

                    new_order_product = OrderProduct(
                        order_id=int(row['order_id']),
                        product_id=int(row['product_id']),
                        add_to_cart_order=int(row['add_to_cart_order']),
                        reordered=reordered
                    )
                    db.add(new_order_product)

    await db.commit()