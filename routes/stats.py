from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func

from database import get_session
from models import Order, OrderStatus

router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)


@router.get("/daily")
def daily_summary(
    summary_date: Optional[str] = Query(
        default=None,
        description="Date for the summary (YYYY-MM-DD)"
    ),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = datetime.now().strftime("%Y-%m-%d")

    start_date = datetime.strptime(
        summary_date,
        "%Y-%m-%d"
    )

    end_date = start_date.replace(
        hour=23,
        minute=59,
        second=59
    )

    summary = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id))
            .where(Order.order_status == status)
            .where(Order.created_at >= start_date)
            .where(Order.created_at <= end_date)
        ).one()

        summary[status.value] = count
        total += count

    return {
        "date": summary_date,
        "summary": summary,
        "total": total
    }