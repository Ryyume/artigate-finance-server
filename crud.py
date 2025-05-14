from sqlalchemy.orm import Session
import models, schemas

# Создание подразделения
def create_subdivision(db: Session, sub: schemas.SubdivisionCreate):
    db_sub = models.Subdivision(name=sub.name)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

# Создание фонда
def create_fund(db: Session, fund: schemas.FundCreate):
    db_fund = models.Fund(**fund.dict(), balance=0.0)
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund

# Создание продажи и автоматическое распределение по фондам
def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    # обновляем балансы фондов
    funds = db.query(models.Fund).filter(models.Fund.subdivision_id == sale.subdivision_id).all()
    for fund in funds:
        fund.balance += sale.amount * fund.percent / 100
    db.commit()

    return db_sale

# Создание расхода
def create_expense(db: Session, exp: schemas.ExpenseCreate):
    db_exp = models.Expense(**exp.dict())
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp
