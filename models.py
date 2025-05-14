from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Subdivision(Base):
    __tablename__ = "subdivisions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    funds = relationship("Fund", back_populates="subdivision")
    sales = relationship("Sale", back_populates="subdivision")

class Fund(Base):
    __tablename__ = "funds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    percent = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)

    subdivision_id = Column(Integer, ForeignKey("subdivisions.id"))
    subdivision = relationship("Subdivision", back_populates="funds")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    subdivision_id = Column(Integer, ForeignKey("subdivisions.id"))
    subdivision = relationship("Subdivision", back_populates="sales")
    expenses = relationship("Expense", back_populates="sale")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)

    sale_id = Column(Integer, ForeignKey("sales.id"))
    sale = relationship("Sale", back_populates="expenses")
