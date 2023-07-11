from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_cursor
from schemas import schemas_dto
from models.Order import Order
import utilities

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

@router.post("", response_model=schemas_dto.Order)
def create_order(
    order: schemas_dto.OrderCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: Session = Depends(get_cursor)
    ):
    try:
        decoded_customer_id = utilities.decode_token(token)
        new_order = Order(
            customer_id = decoded_customer_id,
            camera_id= order.camera_id,
            quantity= order.quantity,
            total_amount= order.total_amount,
            shipping_address= order.shipping_address,
            status= order.status
        )
        cursor.add(new_order)
        cursor.commit()
        cursor.refresh(new_order)
        return new_order
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera {id} dosn't exit can't post order".format(id=order.camera_id)
        )

@router.get("/{order_id}", response_model=schemas_dto.Order)
def get_order(order_id: int, cursor: Session = Depends(get_cursor)):
    order = cursor.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
