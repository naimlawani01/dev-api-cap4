from datetime import datetime
from pydantic import BaseModel, Field
# DTO : Data Transfert Object



class Camera_POST_Body (BaseModel):
    brand : str
    model : str
    resolution: str
    price: float
    description: str
    availability: bool
    rating: float


class Camera_PATCH_Body (BaseModel):
    price: float
    description: str
    availability: bool
    rating: float

class Customer_POST_Body (BaseModel):
    customerEmail:str
    customerPassword: str
    role: str = "visiteur"

class Customer_response (BaseModel):
    id: int
    email:str
    role: str
    create_at: datetime
    class Config: # Importante pour la traduction ORM->DTO
        orm_mode= True

class Customer_PATCH_Body(BaseModel):
    role: str    
        
class OrderBase(BaseModel):
    camera_id: int
    quantity: int
    total_amount: float
    shipping_address: str
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    camera_id: int
    review_text: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):

    class Config:
        orm_mode = True