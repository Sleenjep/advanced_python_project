from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.routes import auth, products, cart, user, recommendations

from src.database.db_init import engine, Base, async_session
from src.database.db_startup import (
    create_default_user,
    create_departments,
    create_aisles,
    create_products,
    create_orders,
    create_order_products,
    create_users_from_orders
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as db:
        await create_default_user(db)
        await create_departments(db)
        await create_aisles(db)
        await create_products(db)
        await create_users_from_orders(db)
        await create_orders(db)
        await create_order_products(db)

