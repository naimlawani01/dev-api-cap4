from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Numeric
from .base import Base


class Camera(Base):
    __tablename__= "camera"
    id = Column(Integer, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    resolution = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    description = Column(String, nullable=False)
    availability = Column(Boolean, nullable=False)
    rating = Column(Numeric, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')