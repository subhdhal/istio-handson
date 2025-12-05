import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db
from .routers import products, customers, orders

APP_VERSION = os.getenv("APP_VERSION", "v1")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {
        "service": "order-service",
        "version": APP_VERSION,
    }


@app.get("/health")

def read_health():
    return {"status": "ok"}

@app.get("/debug/orders_count")
def get_orders_count(db: Session = Depends(get_db)):
    count = db.query(models.Order).count()
    return {"orders_count": count}
