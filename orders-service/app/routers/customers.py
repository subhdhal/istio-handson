from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("/", response_model=schemas.CustomerRead)
def create_customer(
    customer_in: schemas.CustomerCreate,
    db: Session = Depends(get_db),
):
    # Optional: prevent duplicate emails
    existing = crud.get_customer_by_email(db, customer_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db, customer_in)


@router.get("/", response_model=List[schemas.CustomerRead])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.list_customers(db, skip=skip, limit=limit)


@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
