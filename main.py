from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/subdivisions/", response_model=schemas.Subdivision)
def add_subdivision(sub: schemas.SubdivisionCreate, db: Session = Depends(get_db)):
    return crud.create_subdivision(db, sub)

@app.post("/funds/", response_model=schemas.Fund)
def add_fund(fund: schemas.FundCreate, db: Session = Depends(get_db)):
    return crud.create_fund(db, fund)

@app.post("/sales/", response_model=schemas.Sale)
def add_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return crud.create_sale(db, sale)

@app.post("/expenses/", response_model=schemas.Expense)
def add_expense(exp: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, exp)

@app.get("/stats", response_class=HTMLResponse)
def stats(request: Request, db: Session = Depends(get_db)):
    total_sales = db.query(func.sum(models.Sale.amount)).scalar() or 0
    total_expenses = db.query(func.sum(models.Expense.amount)).scalar() or 0
    profit = total_sales - total_expenses
    subdivisions = db.query(models.Subdivision).all()
    funds = db.query(models.Fund).all()
    sales = db.query(models.Sale).all()
    expenses = db.query(models.Expense).all()
    return templates.TemplateResponse("stats.html", {
        "request": request,
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        "profit": profit,
        "subdivisions": subdivisions,
        "funds": funds,
        "sales": sales,
        "expenses": expenses
    })
