from fastapi import FastAPI
from models import Product
from database import session, engine
import database_models

database_models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get("/")
def greet():
    return "welcome to Home page"

products = [
    Product(id=1, name="phone", description="A smartphone", price=99, quantity=10),
    Product(id=2, name="Laptop", description="A Laptop", price=199.99, quantity=50)
]

def init_db():
    db = session()
    for product in products:
        db.add(database_models.Product(**product.model_dump()))
    db.commit()

#init_db()

@app.get("/products")
def get_all_products():
    return products

@app.get("/product/1")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "Requested Product not found"

@app.post("/products")
def add_product(product: Product):
    products.append(product)
    return "Product added successfully"

@app.put("/products")
def update_product(id: int, product: Product):
    for i in range(0, len(products)):
        if products[i].id == id:
            products[i]= product
            return "Product updated successfully"
    return "Product not found"

@app.delete("/product/{id}")
def delete_product_by_id(id : int):
    for i in range(0, len(products)):
        if products[i].id == id:
            del products[i]
            return "Product deleted successfully"
    return "Product not found"