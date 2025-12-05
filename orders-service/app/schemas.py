from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------- Product ----------
class ProductBase(BaseModel):
    name: str
    price: float
    stock_quantity: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- Customer ----------

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- Order/ OrderItem ----------
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    
class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    product_id: int
    quantity: int
    price_per_item: float
    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead] = Field(default_factory=list, alias="order_items")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)