from fastapi import FastAPI
from sqlalchemy import and_, or_
from datetime import datetime

from models import Base, Product
from database import engine, SessionLocal

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Hello FastAPI"}


@app.get("/products")
def get_products(
    limit: int = 20,
    category: str | None = None,
    cursor_time: str | None = None,
    cursor_id: int | None = None
):
    session = SessionLocal()

    try:
        query = session.query(Product)

        # Category filter
        if category:
            query = query.filter(Product.category == category)

        # Cursor pagination
        if cursor_time and cursor_id:

            cursor_dt = datetime.fromisoformat(cursor_time)

            query = query.filter(
                or_(
                    Product.updated_at < cursor_dt,
                    and_(
                        Product.updated_at == cursor_dt,
                        Product.id < cursor_id
                    )
                )
            )

        # Newest first
        query = query.order_by(
            Product.updated_at.desc(),
            Product.id.desc()
        )

        products = query.limit(limit).all()

        result = [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "created_at": p.created_at,
                "updated_at": p.updated_at
            }
            for p in products
        ]

        next_cursor = None

        if products:
            last_product = products[-1]

            next_cursor = {
                "cursor_time": last_product.updated_at.isoformat(),
                "cursor_id": last_product.id
            }

        return {
            "count": len(result),
            "data": result,
            "next_cursor": next_cursor
        }

    finally:
        session.close()