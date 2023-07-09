from fastapi import FastAPI
from models import Camera, Order, Customer, Review
import models # Import des ORM
from app.database import database_engine

# Documentation
from docs.description import api_description
from docs.tags import tags_metadata

#Import des routers
import routers.router_cameras, routers.router_customers, routers.router_auth, routers.router_orders, routers.router_reviews

# Créer les tables si elles ne sont pas présente dans la DB
Camera.Base.metadata.create_all(bind=database_engine)
Customer.Base.metadata.create_all(bind=database_engine)
Order.Base.metadata.create_all(bind=database_engine)
Review.Base.metadata.create_all(bind=database_engine)



#Lancement de l'API
app= FastAPI( 
    title="Snappyshop",
    description=api_description,
    openapi_tags=tags_metadata # tagsmetadata definit au dessus
    )

# Ajouter les routers dédiés
app.include_router(routers.router_cameras.router)
app.include_router(routers.router_customers.router)
app.include_router(routers.router_auth.router)
app.include_router(routers.router_orders.router)
app.include_router(routers.router_reviews.router)