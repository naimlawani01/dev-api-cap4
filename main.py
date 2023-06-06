from contextlib import nullcontext
from typing import Optional
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel
app = FastAPI() # Variable name for the server


cameras = cameras = [
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
class Camera(BaseModel):
    id: int
    brand: str
    model: str
    resolution: str
    price: float
    description: str
    availability: bool = True
    rating: Optional[int]




@app.get("/")
async def root():
    return {"message": "Bingo"}

@app.get("/cameras")
async def getCameras():
    return cameras
#Get by Id
@app.get("/cameras/{camera_id}")
async def getCameraById(camera_id: int, response: Response):
    corresponding_camera = {}
    for item in cameras:
        if item["id"] == camera_id:
            index = cameras.index(item)
            print(index)
            corresponding_camera =  item
            return corresponding_camera
            break
    if corresponding_camera == {}:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Camera not found"}
    
    # try:
    #     corresponding_camera = cameras[index]
    # except:
    #     raise HTTPException(
    #         status.HTTP_404_NOT_FOUND,
    #         detail= "Camera not found"
    #     )


    return corresponding_camera

@app.post("/cameras", status_code=201)
async def createCameras(payload: Camera):
    cameras.append(payload)
    return {"message": "Bingo new camera added successfully: {brand} id: {id}: ".format(brand = payload.brand, id= payload.id)}