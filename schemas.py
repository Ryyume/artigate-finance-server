from pydantic import BaseModel
from datetime import datetime

class SubdivisionBase(BaseModel):
    name: str

class SubdivisionCreate(SubdivisionBase):
    pass

class Subdivision(SubdivisionBase):
    id: int
    class Config:
        from_attributes = True

class FundBase(BaseModel):
    name: str
    percent: float
    subdivision_id: int

class FundCreate(FundBase):
    pass

class Fund(FundBase):
    id: int
    balance: float
    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    name: str
    category: str
    amount: float
    subdivision_id: int

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    title: str
    amount: float
    sale_id: int

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    class Config:
        from_attributes = True