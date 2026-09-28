from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


# Order Status Enum
class OrderStatus(str, Enum):
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


# Database Model
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    customer_name: str
    customer_address: str
    order_items: str

    order_status: OrderStatus = Field(
        default=OrderStatus.preparing
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now}
    )


# Schema for Creating Order
class OrderCreate(SQLModel):
    customer_name: str
    customer_address: str
    order_items: str


# Schema for Updating Order
class OrderUpdate(SQLModel):
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    order_items: Optional[str] = None
    order_status: Optional[OrderStatus] = None


# Schema for Status Log
class StatusLog(SQLModel):
    order_id: int
    order_status: OrderStatus
    new_status: OrderStatus
    changed_at: datetime = Field(
        default_factory=datetime.now
    )