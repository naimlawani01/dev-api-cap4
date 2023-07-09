from contextlib import nullcontext
from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

db_info = {
    "host": "localhost",
    "database":"Snappyshop",
    "user":"postgres",
    "password": "API"}
connexion = psycopg2.connect(
    host="dpg-ci8rn0tgkuvmfnsaa9j0-a.oregon-postgres.render.com",
    database="snappyshop",
    user="imrane",
    password="t6p78CVHWVBM09iEt3IbI9YEMmoGTBfU",
    cursor_factory=RealDictCursor
)


cursor= connexion.cursor() #TODO Faire des trucs

    


description = """
## Snappyshop
    Récupérer la liste de toutes les caméras disponibles.
    Récupérer les détails d'une caméra spécifique en utilisant son ID.
    Ajouter une nouvelle caméra à la liste.
    Supprimer une caméra existante en utilisant son ID.
    Mettre à jour les informations d'une caméra existante en utilisant son ID.

## Gestion des utilisateurs
    Ajouter un nouvel utilisateur à la liste.
    Mettre à jour les informations d'un utilisateur existant en utilisant son ID.
    Récupérer les détails d'un utilisateur spécifique en utilisant son ID.
    Supprimer un utilisateur existant en utilisant son ID.

"""
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "cameras",
        "description": "Manage Cameras. ",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]
app = FastAPI (title="snappyshop",
    openapi_tags=tags_metadata,
    description=description,
) # Variable name for the server


camerasList = [
        {
            "id": 1,
            "brand": "Canon",
            "model": "EOS 5D Mark IV",
            "resolution": "30.4 MP",
            "price": 2499,
            "description": "The Canon EOS 5D Mark IV is a full-frame DSLR camera with impressive image quality and advanced features.",
            "availability": True,
            "rating": 3
        },
        {
            "id": 2,
            "brand": "Nikon",
            "model": "D850",
            "resolution": "45.7 MP",
            "price": 3299,
            "description": "The Nikon D850 is a high-resolution DSLR camera with exceptional dynamic range and speedy performance.",
            "availability": True,
            "rating": 3
        },
        {
            "id": 3,
            "brand": "Sony",
            "model": "Alpha a7 III",
            "resolution": "24.2 MP",
            "price": 1999,
            "description": "The Sony Alpha a7 III is a mirrorless camera that offers impressive low-light performance and excellent autofocus capabilities.",
            "availability": True,
            "rating": 3
        },
        {
            "id": 4,
            "brand": "Fujifilm",
            "model": "X-T4",
            "resolution": "26.1 MP",
            "price": 1799,
            "description": "The Fujifilm X-T4 is a versatile mirrorless camera known for its outstanding image quality and advanced video capabilities.",
            "availability": True,
            "rating": 3
        },
        {
            "id": 5,
            "brand": "Panasonic",
            "model": "Lumix GH5",
            "resolution": "20.3 MP",
            "price": 1699,
            "description": "The Panasonic Lumix GH5 is a professional-grade mirrorless camera with exceptional video capabilities and advanced shooting options.",
            "availability": True,
            "rating": 3
        }
    ]
#Ma petite fonction 
def get_corresponding_camera(id: int):
    for item in camerasList:
        if item["id"] == id:
            index = camerasList.index(item)
            return index
        
class Camera(BaseModel):

    brand: str
    model: str
    resolution: str
    price: float
    description: str
    availability: bool = True
    rating: Optional[int]




@app.get("/", tags=["- root"])
async def root():
    return {"message": "Bingo"}

#Get all camremas 
@app.get("/cameras", tags=["cameras"])
async def get_cameras():
    #Requete SQL
    cursor.execute("SELECT * FROM camera order by id ")
    dbCameras = cursor.fetchall()
    return {
        "cameras": dbCameras,
        "limit": 10,
        "total": len(dbCameras)
    }
#Get cameras by Id
@app.get("/cameras/{camera_id}", tags=["cameras"])
async def get_camera_by_id(camera_id: int, response: Response):
    # corresponding_camera = {}
    # id = get_corresponding_camera(camera_id)
    try: 
        cursor.execute("SELECT * FROM camera WHERE id={id}".format(id = camera_id))
        corresponding_camera = cursor.fetchone()
        if corresponding_camera:
            return corresponding_camera
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )
            
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )
    # if corresponding_camera == {}:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": "Camera not found"}
    # else:
    #     return corresponding_camera
    
    # try:
    #     corresponding_camera = cameras[index]
    # except:
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND,
    #         detail= "Camera not found"
    #     )

# Add cameras
@app.post("/cameras", tags=["cameras"])
async def create_cameras(payload: Camera, response: Response):
    # camerasList.append(payload.dict())
    brand = payload.brand
    model= payload.model
    resolution= payload.resolution
    price= payload.price
    description= payload.description
    availability= payload.availability
    rating= payload.rating
    query = """
        INSERT INTO camera (brand, model, resolution, price, description, availability, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(query, (
        brand,
        model,
        resolution,
        price,
        description,
        availability,
        rating
    ))
    # Validation de la transaction
    connexion.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Bingo new camera added successfully: {brand} ".format(brand = payload.brand)}

#delete cameras
@app.delete("/cameras/{camera_id}", tags=["cameras"])
async def delete_camera(camera_id: int, response: Response):
    # camera_id = str(camera_id)
    # query = "DELETE FROM camera WHERE id= %s"
    # print(camera_id)
    # cursor.execute(query,(camera_id,))
    # connexion.commit()
    # response.status_code = status.HTTP_204_NO_CONTENT
    # return
    try: 
        cursor.execute("SELECT * FROM camera WHERE id={id}".format(id = camera_id))
        corresponding_camera = cursor.fetchone()
        if corresponding_camera:
            camera_id = str(camera_id)
            query = "DELETE FROM camera WHERE id= %s"
            print(camera_id)
            cursor.execute(query,(camera_id,))
            connexion.commit()
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )
            
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )
    # corresponding_camera = get_corresponding_camera(camera_id)
    # camerasList.pop(corresponding_camera)
     

# PUT (Remplacer update cameras- > id)
@app.put("/cameras/{camera_id}", tags=["cameras"])
async def update_camera(camera_id: int, payload: Camera,response: Response):
    brand = payload.brand
    model= payload.model
    resolution= payload.resolution
    price= payload.price
    description= payload.description
    availability= payload.availability
    rating= payload.rating
    try:
        cursor.execute("SELECT * FROM camera WHERE id={id}".format(id = camera_id))
        corresponding_camera = cursor.fetchone()
        if corresponding_camera:
            query= """UPDATE camera
            SET brand = %s,
            model= %s,
            resolution= %s,
            price= %s,
            description= %s,
            availability= %s,
            rating= %s
            WHERE id= %s;"""
            cursor.execute(query,(brand,
            model,
            resolution,
            price,
            description,
            availability,
            rating, 
            camera_id))
            connexion.commit()
            return {"messag": "Bingo cammera updated successfuly: {camera_brand}".format(camera_brand= payload.brand)}
        else:
            raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found"
        )         
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "Camera not found yoo"
        )
    # corresponding_camera = get_corresponding_camera(camera_id)
    # camerasList[corresponding_camera]= payload.dict()
    

 



# USER 

class User(BaseModel):
    id: int
    username: str
    password: str

#Ma petite fonction 
def get_corresponding_user(id: int):
    for item in user_list:
        if item["id"] == id:
            index = user_list.index(item)
            return index

user_list = []
#Add user
@app.post("/users", tags=["users"])
async def create_user(payload: User, response: Response):
    user_list.append(payload.dict())
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Bingo new user added successfully: {username} : ".format(username = payload.username)}

#update user
@app.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: int,payload: User, response: Response):
    corresponding_user = get_corresponding_user(user_id)
    user_list[corresponding_user]= payload.dict()
    return {"messag": "Bingo cammera updated successfuly: {username}".format(payload.username)}

#User by Id
@app.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id: int, response: Response):
    corresponding_user = {}
    id = get_corresponding_user(user_id)
    try: 
        corresponding_user = user_list[id]
        return corresponding_user
    except:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= "User not found"
        )
    

#Delete user 
@app.delete("/users/{user_id}", tags=["users"])
async def delete_camera(user_id: int, response: Response):
    corresponding_user = get_corresponding_user(user_id)
    user_list.pop(corresponding_user)
    response.status_code = status.HTTP_204_NO_CONTENT
    return 