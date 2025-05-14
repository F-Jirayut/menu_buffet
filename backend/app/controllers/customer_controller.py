

from app.models import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String
from typing import Dict, Optional

def get_customers(db: Session, search: Optional[str] = None):
    query = db.query(Customer)

    if search:
        search_like = f"%{search}%"
        query = query.filter(
            or_(
                cast(Customer.id, String).like(search_like),
                Customer.name.like(search_like)
            )
        )

    return query.customer_by(Customer.sort_customer).all()

def get_customer_by_name(db: Session, name: str):
    return db.query(Customer).filter(Customer.name == name).first()

def get_customer_by_id(db: Session, id: int):
    return db.query(Customer).filter(Customer.id == id).first()

def create_customer(db: Session, customer: CustomerCreate):
    existing_customer = db.query(Customer).filter(
        (Customer.phone == customer.phone) | (Customer.email == customer.email)
    ).first()

    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this phone or email already exists")

    
    db_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
    )

    db.add(db_customer)

    try:
        db.commit()
        db.refresh(db_customer)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error creating customer: {str(e)}")

    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate) -> Customer:
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_customer = db.query(Customer).filter(
        (Customer.phone == customer.phone) | (Customer.email == customer.email)
    ).filter(Customer.id != customer_id).first()

    if existing_customer:
        raise HTTPException(status_code=400, detail="Phone or email already exists")

    try:
        db_customer.name = customer.name
        db_customer.phone = customer.phone
        db_customer.email = customer.email
        db.commit()
        db.refresh(db_customer)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error updating customer")
    return db_customer

def delete_customer(db: Session, customer_id: int) -> Dict[str, str]:
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    try:
        db.delete(db_customer)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting customer")
    
    return {"message": "Customer deleted successfully"}