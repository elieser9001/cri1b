from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import func
from .database import Base

class License(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(200))
    name = Column(String(200))
    lastname = Column(String(200))
    email = Column(String(200))
    phone_number = Column(String(200))
    expired_time = Column(DateTime)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(200))
    email = Column(String(200))
    key = Column(String(200))
    ext_id = Column(String(200))
    __table_args__ = (UniqueConstraint('customer_id', 'key', name='customer_id_key'),)
