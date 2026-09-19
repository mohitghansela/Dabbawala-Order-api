from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func

from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


# CREATE
@router.post("/", response_model=ReviewRead)
def create_review(
    review: ReviewCreate,
    session: Session = Depends(get_session)
):
    db_review = Review(**review.model_dump())

    session.add(db_review)
    session.commit()
    session.refresh(db_review)

    return db_review


# READ ALL
@router.get("/", response_model=list[ReviewRead])
def get_reviews(
    session: Session = Depends(get_session)
):
    reviews = session.exec(select(Review)).all()
    return reviews


# READ ONE
@router.get("/{review_id}", response_model=ReviewRead)
def get_review(
    review_id: int,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


# UPDATE
@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: Session = Depends(get_session)
):
    db_review = session.get(Review, review_id)

    if not db_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    review_data = review_update.model_dump(exclude_unset=True)

    for key, value in review_data.items():
        setattr(db_review, key, value)

    session.add(db_review)
    session.commit()
    session.refresh(db_review)

    return db_review


# DELETE
@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    session.delete(review)
    session.commit()

    return {
        "message": f"Review {review_id} deleted successfully"
    }


# AVERAGE RATING
@router.get("/stats/average-rating")
def get_average_rating(
    session: Session = Depends(get_session)
):
    average_rating = session.exec(
        select(func.avg(Review.rating))
    ).one()

    return {
        "average_rating": round(float(average_rating), 2) if average_rating else 0
    }