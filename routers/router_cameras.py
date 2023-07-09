from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_cursor
from schemas import schemas_dto
from models.Camera import Camera
from models.Customer import Customer
import utilities

from pydantic.typing import Annotated
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter(
    prefix='/cameras',
    tags=['Cameras']
)

#Get all cameras
@router.get("")
async def get_cameras(
    cursor: Session= Depends(get_cursor),
    limit: int=10, 
    offset: int=0
    ):
    all_cameras = cursor.query(Camera).limit(limit).offset(offset).all() # Get limit Camera 
    camera_count= cursor.query(func.count(Camera.id)).scalar() #Count total camera in DB
    return {
        "products": all_cameras,
        "limit": limit,
        "total": camera_count,
        "skip": offset
    } 
#Get cameras by Id
@router.get("/{camera_id}")
async def get_camera_by_id(camera_id: int, response: Response, cursor: Session= Depends(get_cursor)):
    # corresponding_camera = {}
    # id = get_corresponding_camera(camera_id)

    corresponding_camera = cursor.query(Camera).filter_by(id = camera_id).first() # Filter Camera 
    if not corresponding_camera: # Raise error if there is not camera
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )
    return corresponding_camera


#Post Camera

@router.post("", status_code= status.HTTP_201_CREATED)
async def create_cameras(
    payload: schemas_dto.Camera_POST_Body,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session= Depends(get_cursor)
    ):
    # Le décodage du token permet de récupérer l'identifiant du customer
    decoded_customer_id = utilities.decode_token(token)
    new_camera = Camera(
        brand = payload.brand,
        model = payload.model,
        resolution = payload.resolution,
        price = payload.price,
        description = payload.description,
        availability = payload.availability,
        rating = payload.rating
    ) # build the insert
    cursor.add(new_camera) # Send the query
    cursor.commit() #Save the staged change
    cursor.refresh(new_camera)
    return {"message": "Bingo new camera {brand} added successfully with id: {id} ".format(brand = new_camera.brand, id= new_camera.id)}


#Delete camera

@router.delete('/{camera_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
    camera_id:int,
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor:Session=Depends(get_cursor)
    ):
    
    decoded_customer_id = utilities.decode_token(token)
    corresponding_customer = cursor.query(Customer).filter(Customer.id == decoded_customer_id).first()
    # print(corresponding_customer)
        
    if corresponding_customer.role == "admin": 
        # Recherce si la camera existe 
        corresponding_camera = cursor.query(Camera).filter_by(id = camera_id)
        if corresponding_camera.first():
            # Continue to delete
            corresponding_camera.delete() # supprime
            cursor.commit() # commit the stated changes (changement latent)
            return 
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found with id: {id} ".format(id= camera_id)
        ) 
    else:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail= "l'utilisateur n'est pas autorisé"
        )
    # except:
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND,
    #         detail= "Camera not found with id: {id} ".format(id= camera_id)
    #     )
    

# Update
@router.patch('/{camera_id}')
async def update_camera(camera_id: int, payload:schemas_dto.Camera_PATCH_Body, cursor:Session=Depends(get_cursor)):
    # Recherce si la camera existe  
    corresponding_camera = cursor.query(Camera).filter_by(id = camera_id)
    if corresponding_camera.first():
        # mise à jour (quoi avec quelle valeur ?) Body -> DTO
        corresponding_camera.update({
            "price": payload.price,
            "description": payload.description,
            "availability": payload.availability,
            "rating": payload.rating
        })
        cursor.commit() #Save modification
        return corresponding_camera.first()
    else: 
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Ne corresponding product with id: {camera_id}'
        )