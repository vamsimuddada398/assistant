from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware
import os

# =========================
# DATABASE CONFIG
# =========================

DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "vamsi"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =========================
# TABLE MODEL
# =========================

class Customer(Base):
    __tablename__ = "customer"

    transaction_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    product_category = Column(String(100))
    product_name = Column(String(200))
    units_sold = Column(Integer)
    unit_price = Column(Float)
    total_revenue = Column(Float)
    region = Column(String(100))
    payment_method = Column(String(50))

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DB Dependency
# =========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# API ENDPOINTS
# =========================

# Get all customers (limit 100)
@app.get("/")
def home():
    return {"message":"api is running successfully"}

@app.get("/customers/{region_name}")
def get_customers(region_name: str, db: Session = Depends(get_db)):
    customers = db.query(Customer).filter(Customer.region == region_name).all()
    result = []
    for c in customers:
        result.append({
            "transaction_id": c.transaction_id,
            "date": str(c.date),
            "product_category": c.product_category,
            "product_name": c.product_name,
            "units_sold": c.units_sold,
            "unit_price": c.unit_price,
            "total_revenue": c.total_revenue,
            "region": c.region,
            "payment_method": c.payment_method
        })
    return result


# Get by region
@app.get("/customers/region/{region_name}")
def get_by_region(region_name: str, db: Session = Depends(get_db)):
    data = db.query(Customer).filter(Customer.region == region_name).all()
    return data


# Get by product name
@app.get("/customers/product/{product_name}")
def get_by_product(product_name: str, db: Session = Depends(get_db)):
    data = db.query(Customer).filter(Customer.product_name == product_name).all()
    return data


# Get total revenue by region
@app.get("/revenue/{region_name}")
def total_revenue(region_name: str, db: Session = Depends(get_db)):
    data = db.query(Customer).filter(Customer.region == region_name).all()

    total = sum([row.total_revenue for row in data])

    return {
        "region": region_name,
        "total_revenue": total
    }
