from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from database import get_session
from models import (
    Order,
    OrderCreate,
    OrderStatus,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=Order)
async def create_order(
    order: OrderCreate,
    session: Session = Depends(get_session)
):
    db_order = Order(**order.model_dump())

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order


@router.get("/", response_model=list[Order])
def list_orders(
    status: Optional[OrderStatus] = Query(
        default=None,
        description="Filter orders by status"
    ),
    created_date: Optional[str] = Query(
        default=None,
        description="Filter orders by creation date (YYYY-MM-DD)"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):

    query = session.query(Order)

    if status:
        query = query.filter(Order.order_status == status)

    if created_date:
        date_obj = datetime.strptime(
            created_date,
            "%Y-%m-%d"
        ).date()

        start_date = datetime.combine(
            date_obj,
            datetime.min.time()
        )

        end_date = datetime.combine(
            date_obj,
            datetime.max.time()
        )

        query = query.filter(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        )

    query = query.offset(skip).limit(limit)

    return query.all()