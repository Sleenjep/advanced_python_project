from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database.db_init import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    aisle_id = Column(Integer, ForeignKey("aisles.id", ondelete="CASCADE"), nullable=False)

    aisle = relationship("Aisle", back_populates="products")
    department = relationship("Department", back_populates="products")
    order_products = relationship("OrderProduct", back_populates="product", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    cart = relationship("Cart", back_populates="user", cascade="all, delete-orphan")

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quantity = Column(Integer, default=1)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    product = relationship("Product")
    user = relationship("User", back_populates="cart")

    __table_args__ = (
        UniqueConstraint('product_id', 'user_id', name='unique_cart_item'),
    )

class Aisle(Base):
    __tablename__ = "aisles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    products = relationship("Product", back_populates="aisle", cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    products = relationship("Product", back_populates="department", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    eval_set = Column(String, nullable=False)
    order_number = Column(Integer, nullable=False)
    order_dow = Column(Integer, nullable=False)
    order_hour_of_day = Column(Integer, nullable=False)
    days_since_prior_order = Column(Float, nullable=True)

    user = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")

class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    add_to_cart_order = Column(Integer, nullable=False)
    reordered = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")