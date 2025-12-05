from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/", response_model=schemas.ProductRead)
def create_product(
    product_in: schemas.ProductCreate,
    db: Session = Depends(get_db),
):
    return crud.create_product(db, product_in)


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.list_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
