from fastapi import FastAPI
from models import Camera, Order, Customer, Review
import models # Import des ORM
from app.database import database_engine

#Import des routers
import routers.router_cameras, routers.router_customers, routers.router_auth, routers.router_orders, routers.router_reviews

# Créer les tables si elles ne sont pas présente dans la DB
Camera.Base.metadata.create_all(bind=database_engine)
Customer.Base.metadata.create_all(bind=database_engine)
Order.Base.metadata.create_all(bind=database_engine)
Review.Base.metadata.create_all(bind=database_engine)


api_description = description = """
Watch API helps you do awesome stuff. 🚀

## Products

You will be able to:

* Create new product.
* Get products list.
"""

# Liste des tags utilises dans la doc
tags_metadata = [
    {
        "name": "Cameras",
        "description": "Manage Products. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Customers",
        "description": "Create and list customers of our API",
    },
]

#Lancement de l'API
app= FastAPI( 
    title="Watch API",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadata definit au dessus
    )

# Ajouter les routers dédiés
app.include_router(routers.router_cameras.router)
app.include_router(routers.router_customers.router)
app.include_router(routers.router_auth.router)
app.include_router(routers.router_orders.router)
app.include_router(routers.router_reviews.router)