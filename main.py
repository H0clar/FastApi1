from fastapi import FastAPI, HTTPException
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from fastapi import Depends

from sqlalchemy.orm import Session
from fastapi import Depends

from models.products import Product

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir la tabla de productos
class DBProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

# Inyectar el modelo Pydantic en el modelo de base de datos SQLAlchemy
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Función para obtener todos los productos
def get_products(db, skip: int = 0, limit: int = 10):
    return db.query(DBProduct).offset(skip).limit(limit).all()

# Función para crear un nuevo producto
def create_product(db, product: Product):
    db_product = DBProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Rutas de la API
@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 10, db: SessionLocal = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@app.post("/products/", response_model=Product)
def create_product(product: Product, db: SessionLocal = Depends(get_db)):
    return create_product(db, product)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product, db: SessionLocal = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for var, value in vars(product).items():
        setattr(db_product, var, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: SessionLocal = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)




