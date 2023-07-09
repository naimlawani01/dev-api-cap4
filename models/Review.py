from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Numeric
from .base import Base

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    camera_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    review_text = Column(String, nullable=False)