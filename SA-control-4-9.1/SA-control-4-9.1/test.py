from app.database import SessionLocal
from app.models import Product

db = SessionLocal()

p1 = Product(title="Phone", price=500, count=10)
p2 = Product(title="Laptop", price=1500, count=5)

db.add_all([p1, p2])
db.commit()