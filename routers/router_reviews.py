from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_cursor
from schemas import schemas_dto
from models.Review import Review
from models.Customer import Customer
import utilities
from typing import List

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


router = APIRouter(
    prefix='/reviews',
    tags=['Reviews']
)

#Get all review
@router.get('', response_model=List[schemas_dto.Review])
async def get_all_reviews(
    cursor: Session = Depends(get_cursor)
    ):
    all_reviews = cursor.query(Review).all()  #Query Get all customer
    return all_reviews
#Add  review (AVIS)
@router.post("", response_model=schemas_dto.Review)
def create_review(
    review: schemas_dto.ReviewCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(get_cursor)
    ):
    decoded_customer_id = utilities.decode_token(token) #GET AUTH ID 
    new_review = Review(
        customer_id = decoded_customer_id,
        camera_id = review.camera_id,
        review_text = review.review_text
    ) #Bluid object
    
    # print(new_review)
    cursor.add(new_review)
    cursor.commit() # Save modificationn
    cursor.refresh(new_review)
    return new_review

#Get review by id
@router.get("/{review_id}", response_model=schemas_dto.Review)
def get_review(review_id: int, cursor: Session = Depends(get_cursor)):
    review = cursor.query(Review).filter(Review.id == review_id).first() #FILTER REVIEW BY ID
    if not review: #Check s'il exite un review 
        raise HTTPException(status_code=404, detail="Review not found")
    return review

#Delete review
@router.delete('/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
    review_id:int,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session=Depends(get_cursor)
    ):
    
    decoded_customer_id = utilities.decode_token(token)
    auth_user = cursor.query(Customer).filter(Customer.id == decoded_customer_id).first()
    # print(corresponding_customer)
        
    if auth_user.role == "admin":  #Only admin can delete review
        # Recherce si la camera existe 
        corresponding_review = cursor.query(Review).filter_by(id = review_id)
        if corresponding_review.first():
            # Continue to delete
            corresponding_review.delete() # supprime
            cursor.commit() # commit the stated changes (changement latent)
            return 
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Review not found with id: {id} ".format(id= review_id)
        ) 
    else:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail= "l'utilisateur n'est pas autorisé a supprimer cet aviss"
        )
    # except:
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND,
    #         detail= "Camera not found with id: {id} ".format(id= camera_id)
    #     )
 