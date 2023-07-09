from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import database
from schemas import schemas_dto
from models.Customer import Customer
import utilities

router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)

@router.post('', response_model=schemas_dto.Customer_response, status_code= status.HTTP_201_CREATED)
async def create_customer(
    payload: schemas_dto.Customer_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        hashed_password = utilities.hash_password(payload.customerPassword)
        new_customer= Customer(password=hashed_password, email= payload.customerEmail)
        cursor.add(new_customer) # Send query
        cursor.commit() # Save the staged changes
        cursor.refresh(new_customer) # Pour obtenir l'identifiant
        # return {'message':f'The customer has been created with the id: {new_customer.id}'}
        return new_customer # not a python dict -> donc il faut un mapping
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists" 
        )
    
@router.get('', response_model=list[schemas_dto.Customer_response])
async def get_all_customers(cursor: Session = Depends(database.get_cursor)):
    all_customers = cursor.query(Customer).all()
    return all_customers

@router.get('/{customer_id}', response_model=schemas_dto.Customer_response)
async def get_user_by_id(customer_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_customer = cursor.query(Customer).filter(Customer.id == customer_id).first()
    if(corresponding_customer):
        return corresponding_customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{customer_id}'
        )