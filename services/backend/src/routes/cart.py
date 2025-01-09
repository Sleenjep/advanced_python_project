from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

from src.database.db_models import Cart, Product, User
from src.database.db_init import get_db

router = APIRouter()

@router.post("/add_to_cart")
async def add_to_cart(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        return {"error": "Product not found"}

    result = await db.execute(select(Cart).where(Cart.user_id == user.id, Cart.product_id == product_id))
    cart_item = result.scalars().first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=user.id, product_id=product_id, quantity=quantity)
        db.add(new_cart_item)

    await db.commit()
    return {"message": f"Product {product.name} added to cart"}

@router.get("/get_cart")
async def get_cart(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}

    result = await db.execute(select(Cart).options(joinedload(Cart.product)).where(Cart.user_id == user.id))
    cart_items = result.scalars().all()

    if not cart_items:
        return {"cart": []}

    return {
        "cart": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": item.product.name,
                "price": item.product.price
            }
            for item in cart_items
        ]
    }

@router.post("/delete_from_cart")
async def delete_from_cart(
    request: Request,
    product_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}

    result = await db.execute(select(Cart).where(Cart.user_id == user.id, Cart.product_id == product_id))
    cart_item = result.scalars().first()
    if not cart_item:
        return {"error": "Product not found in cart"}

    await db.delete(cart_item)
    await db.commit()
    return {"message": f"Product with ID {product_id} removed from cart"}

@router.post("/increment_quantity")
async def increment_quantity(
    request: Request,
    product_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    return await add_to_cart(request=request, product_id=product_id, quantity=1, db=db)

@router.post("/decrement_quantity")
async def decrement_quantity(
    request: Request,
    product_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}

    result = await db.execute(select(Cart).where(Cart.user_id == user.id, Cart.product_id == product_id))
    cart_item = result.scalars().first()
    if not cart_item:
        return {"error": "Product not found in cart"}

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        await db.commit()
        return {"message": f"Quantity of product with ID {product_id} decremented by 1"}
    else:
        await db.delete(cart_item)
        await db.commit()
        return {"message": f"Product with ID {product_id} removed from cart"}

@router.get("/generate_receipt")
async def generate_receipt(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    username = request.session.get("user")
    if not username:
        return {"error": "User not logged in"}

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}

    result = await db.execute(select(Cart).options(joinedload(Cart.product)).where(Cart.user_id == user.id))
    cart_items = result.scalars().all()
    if not cart_items:
        return {"error": "Cart is empty"}

    buffer = BytesIO()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Receipt for {user.username}", ln=True, align="C")
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    page_width = pdf.w - 2 * pdf.l_margin
    col_widths = [page_width * 0.35, (page_width * 0.65) / 3, (page_width * 0.65) / 3, (page_width * 0.65) / 3]
    pdf.cell(col_widths[0], 10, "Product Name", border=1, align="C")
    pdf.cell(col_widths[1], 10, "Quantity", border=1, align="C")
    pdf.cell(col_widths[2], 10, "Price", border=1, align="C")
    pdf.cell(col_widths[3], 10, "Total", border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", size=12)
    total_price = 0

    for item in cart_items:
        total_item_price = item.product.price * item.quantity
        pdf.cell(col_widths[0], 10, item.product.name, border=1)
        pdf.cell(col_widths[1], 10, str(item.quantity), border=1, align="C")
        pdf.cell(col_widths[2], 10, f"${item.product.price:.2f}", border=1, align="C")
        pdf.cell(col_widths[3], 10, f"${total_item_price:.2f}", border=1, align="C")
        pdf.ln()
        total_price += total_item_price

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(col_widths[0] + col_widths[1] + col_widths[2], 10, "Total Price" + "\t"*7, border=1, align="R")
    pdf.cell(col_widths[3], 10, f"${total_price:.2f}", border=1, align="C")
    pdf_output = pdf.output(dest='S').encode('latin1')

    file_name = f"receipt_{user.username}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    buffer.write(pdf_output)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )