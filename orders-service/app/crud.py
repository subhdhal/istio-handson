from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Products ----------

def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def list_products(db: Session, skip: int = 0, limit: int = 100) -> list[models.Product]:
    return (
        db.query(models.Product)
        .order_by(models.Product.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# ---------- Customers ----------

def create_customer(db: Session, customer_in: schemas.CustomerCreate) -> models.Customer:
    customer = models.Customer(**customer_in.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_customer(db: Session, customer_id: int) -> models.Customer | None:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> models.Customer | None:
    return db.query(models.Customer).filter(models.Customer.email == email).first()


def list_customers(db: Session, skip: int = 0, limit: int = 100) -> list[models.Customer]:
    return (
        db.query(models.Customer)
        .order_by(models.Customer.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# ---------- Orders ----------

def create_order(db: Session, order_in: schemas.OrderCreate) -> models.Order:
    # 1) Check customer exists
    customer = get_customer(db, order_in.customer_id)
    if not customer:
        raise ValueError("Customer not found")

    # 2) Create empty order first
    order = models.Order(
        customer_id=customer.id,
        status="pending",
        total_amount=0.0,
    )
    db.add(order)

    total_amount = 0.0

    # 3) For each item: check product, stock, adjust, create OrderItem
    for item_in in order_in.items:
        product = get_product(db, item_in.product_id)
        if not product:
            raise ValueError(f"Product {item_in.product_id} not found")

        if product.stock_quantity < item_in.quantity:
            raise ValueError(
                f"Not enough stock for product {product.id} "
                f"(have {product.stock_quantity}, need {item_in.quantity})"
            )

        product.stock_quantity -= item_in.quantity

        order_item = models.OrderItem(
            order=order,
            product_id=product.id,
            quantity=item_in.quantity,
            price_per_item=product.price,
        )
        db.add(order_item)

        total_amount += product.price * item_in.quantity

    order.total_amount = total_amount

    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> models.Order | None:
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def list_orders(db: Session, skip: int = 0, limit: int = 100) -> list[models.Order]:
    return (
        db.query(models.Order)
        .order_by(models.Order.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
