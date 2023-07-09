from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_cursor
from schemas import schemas_dto
from models.Review import Review
import utilities

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


router = APIRouter(
    prefix='/reviews',
    tags=['Reviews']
)


@router.post("", response_model=schemas_dto.Review)
def create_review(
    review: schemas_dto.ReviewCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(get_cursor)
    ):
    decoded_customer_id = utilities.decode_token(token)
    new_review = Review(
        customer_id = decoded_customer_id,
        camera_id = review.camera_id,
        review_text = review.review_text
    )
    
    print(new_review)
    cursor.add(new_review)
    cursor.commit()
    cursor.refresh(new_review)
    return new_review

@router.get("/{review_id}", response_model=schemas_dto.Review)
def get_review(review_id: int, cursor: Session = Depends(get_cursor)):
    review = cursor.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review