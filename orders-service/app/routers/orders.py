from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", response_model=schemas.OrderRead)
def create_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(get_db),
):
    try:
        return crud.create_order(db, order_in)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.list_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
