from database import SessionLocal
from models import Product
from faker import Faker
from datetime import datetime
import random

fake = Faker()

session = SessionLocal()

categories = [
    "Electronics",
    "Books",
    "Fashion",
    "Sports",
    "Furniture"
]

BATCH_SIZE = 5000
TOTAL_PRODUCTS = 200000

for start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):

    products = []

    for _ in range(BATCH_SIZE):

        product = Product(
            name=fake.word(),
            category=random.choice(categories),
            price=round(random.uniform(10, 1000), 2),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        products.append(product)
    #Important: Use bulk_save_objects for better performance when inserting large batches
    
    session.bulk_save_objects(products)
    session.commit()

    print(f"Inserted {start + BATCH_SIZE}")

session.close()