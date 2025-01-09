from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from src.database.db_models import Product, Department, Aisle
from src.database.db_init import get_db
from src.routes.auth import get_user_from_session

router = APIRouter()

@router.post("/add_product")
async def add_product(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    department: int = Form(...),
    aisle: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_from_session(request, db)
    if user is None:
        return {"error": "User is not logged in"}

    department_obj = await db.execute(select(Department).where(Department.id == department))
    department_obj = department_obj.scalars().first()

    aisle_obj = await db.execute(select(Aisle).where(Aisle.id == aisle))
    aisle_obj = aisle_obj.scalars().first()

    if not department_obj or not aisle_obj:
        return {"error": "Invalid department or aisle ID", 
                "aisle_obj": aisle_obj, 
                "department_obj": department_obj}

    new_product = Product(
        name=name,
        price=price,
        department_id=department,
        aisle_id=aisle,
    )
    db.add(new_product)
    await db.commit()

    return {"message": f"Product '{name}' was added successfully"}

@router.post("/delete_product")
async def delete_product(
    request: Request,
    product_id: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user_from_session(request, db)
    if user is None:
        return {"error": "User is not logged in"}

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()

    if not product:
        return {"error": "Product not found"}

    await db.delete(product)
    await db.commit()

    result = await db.execute(select(Product))
    products = result.scalars().all()

    return {
        "message": f"Product '{product.name}' deleted",
        "products": products,
    }

@router.get("/get_all_products")
async def get_all_products(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Product))
        products = result.scalars().all()

        if not products:
            return {"error": "No products found"}

        return {"products": products}

    except Exception as e:
        return {"error": str(e)}