from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Numeric
from .base import Base

class Customer(Base):
    __tablename__="customer"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default='visiteur')
    create_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')