from fastapi import Depends,FastAPI
from models import Product
from database import session , engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware  


database_models.Base.metadata.create_all(bind = engine)

app = FastAPI() #creates the main FastAPI application object that handles all your API routes and requests.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")  # defines a GET API endpoint for the root URL (/) that runs the function below it when that URL is accessed.

def greet():
    return "Welcome to the e-commers"

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=5, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=6, name="Table", description="A wooden table", price=199.99, quantity=20),
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

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

init_db()

@app.get("/products")
def get_all_products(db : Session = Depends(get_db)):
    #db = session()
    #db.query()
    db = db.query(database_models.Product).all()
    return db

@app.get("/products/{id}")                 #here id is dynamic variable 
def get_product_by_id(id : int,db : Session = Depends(get_db)):
    
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first( )
    if db_product:
        return db_product
    return "product is not found"

@app.post("/products")
def add_product(product : Product,db : Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id : int, product : Product,db : Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated successfully"
    return "product not found"

@app.delete("/products/{id}")
def delete_product(id : int,db : Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted successfully"
    return "product not found"




