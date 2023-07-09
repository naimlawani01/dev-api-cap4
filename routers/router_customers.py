from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import database
from schemas import schemas_dto
from models.Customer import Customer
from models.Order import Order
import utilities
from typing import List

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)


#Create custumer
@router.post('', response_model=schemas_dto.Customer_response, status_code= status.HTTP_201_CREATED)
async def create_customer(
    payload: schemas_dto.Customer_POST_Body, 
    cursor: Session = Depends(database.get_cursor),
    ):
    try: 
        hashed_password = utilities.hash_password(payload.customerPassword)
        new_customer= Customer(password=hashed_password, email= payload.customerEmail, role= payload.role)
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
#Get all custumer
@router.get('', response_model=List[schemas_dto.Customer_response])
async def get_all_customers(
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(database.get_cursor)
    ):
    all_customers = cursor.query(Customer).all()  #Query Get all customer
    return all_customers
#Get custumer by ID
@router.get('/{customer_id}', response_model=schemas_dto.Customer_response)
async def get_user_by_id(customer_id:int, cursor: Session = Depends(database.get_cursor)):
    corresponding_customer = cursor.query(Customer).filter(Customer.id == customer_id).first() # Recher du customer correspondant
    if(corresponding_customer): # Check si le customer exist
        return corresponding_customer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user with id:{customer_id}'
        )
#Udpate custumer

@router.patch('/{customer_id}')
async def update_customer(
    customer_id: int, 
    payload:schemas_dto.Customer_PATCH_Body,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session=Depends(database.get_cursor)
    ):
    
    decoded_customer_id = utilities.decode_token(token)
    auth_user = cursor.query(Customer).filter_by(id = decoded_customer_id).first() #Recupération de l'utilisateur connecté
    print(auth_user.role)
    if auth_user.role == "admin": #Check if admin
        # Recherce si l'utilissateur existe  
        corresponding_customer = cursor.query(Customer).filter_by(id = customer_id)
        if corresponding_customer.first():
            # mise à jour (quoi avec quelle valeur ?) Body -> DTO
            corresponding_customer.update({
                "role": payload.role
            })
            cursor.commit()
            return corresponding_customer.first()
        else: 
            raise HTTPException (
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Ne corresponding product with id: {camera_id}'
            )
    else:
       raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail= "User not alowed to do this operation"
            )
       
       
       
       
#Get all custumer orders
@router.get('{customer_id}/orders', response_model=List[schemas_dto.Customer_response])
async def get_all_customers(
    customer_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(database.get_cursor)
    ):
    decoded_customer_id = utilities.decode_token(token)
    auth_user = cursor.query(Customer).filter_by(id = decoded_customer_id).first() #Recupération de l'utilisateur connecté
    if customer_id == decoded_customer_id or auth_user.role == "admin": # Seul l'utilisateur connecté ou L'admin a le droit de consulter ses Order
        all_customer_orders = cursor.query(Order).filter(Order.customer_id == decoded_customer_id).all()
        return all_customer_orders
    else: # Sinon générer une erreur
        raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail= "User not allowed to get these Order "  
            )