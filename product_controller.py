from fastapi import FastAPI, Depends
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

database_models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

@app.get("/")
def greet():
    return "welcome to Home page"

products = [
    Product(id=1, name="phone", description="A smartphone", price=99, quantity=10),
    Product(id=2, name="Laptop", description="A Laptop", price=199.99, quantity=50),
    Product(id=3, name="Keyboard", description="used for typing", price=10, quantity=60),
    Product(id=4, name="mouse", description="click operations", price=5, quantity=70),
    Product(id=5, name="Laptop table", description="workdesk for comfortable working", price=50.99, quantity=30),
    Product(id=6, name="ear pods", description="music time", price=78.34, quantity=100)
]

def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count==0 : 
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

init_db()

@app.get("/products")
def get_all_products(db : Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product: 
        return db_product
    return "Requested Product not found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product added successfully"

@app.put("/products")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db.commit()
            return "Product updated successfully"
    else : 
        return "Product not found"

@app.delete("/product/{id}")
def delete_product_by_id(id : int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id). first()
    if db_product: 
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else: 
        return "Product not found"