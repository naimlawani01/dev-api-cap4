from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from .base import Base

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    camera_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Numeric, nullable=False)
    shipping_address = Column(String, nullable=False)
    status = Column(String, nullable=False)