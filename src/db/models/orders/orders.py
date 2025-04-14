from datetime import date
from decimal import Decimal

from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.metadata import Base
from db.models.orders.base import SCHEMA


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (
        UniqueConstraint("name", "size", postgresql_nulls_not_distinct=True),
        {"schema": SCHEMA},
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    name: Mapped[str]
    size: Mapped[Decimal]
    price: Mapped[Decimal]
    available: Mapped[str]  # JSON string


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": SCHEMA}
    id: Mapped[int] = mapped_column(primary_key=True)
    shop: Mapped[str]
    date: Mapped[date]
    handled: Mapped[bool] = mapped_column(default=False)
    price: Mapped[Decimal] = mapped_column(nullable=True, default=None)
    note: Mapped[str]
    items: Mapped[list["OrderItem"]] = relationship(
        lazy="selectin",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)
    quantity: Mapped[int]
    checked: Mapped[bool] = mapped_column(default=False)
    prepared_quantity: Mapped[int] = mapped_column(default=0)
    note: Mapped[str]
    order_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.orders.id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.items.id"), primary_key=True
    )
    order: Mapped["Order"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship()
