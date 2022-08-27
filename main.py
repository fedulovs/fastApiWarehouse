from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


inventory = {}


@app.get("/get-items")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Inventory).all()


@app.get("/get-item/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(models.Inventory).filter(models.Inventory.id == item_id).first()


@app.get("/get-by-name/{item_name}")
def get_item(name: str, db: Session = Depends(get_db)):
    item_model = db.query(models.Inventory).filter(models.Inventory.name == name).first()

    if item_model is None:
        raise HTTPException(
            status_code=404,
            detail="Item " + name + " does not exist."
        )

    return item_model


@app.post("/create-item")
def create_item_in_db(item: Item, db: Session = Depends(get_db)):
    item_model = models.Inventory()

    item_model.name = item.name
    item_model.price = item.price
    item_model.brand = item.brand

    db.add(item_model)
    db.commit()

    return {"Data": "Item " + item.name + " was added to inventory"}


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    item_model = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code=404,
            detail="Item ID does not exist."
        )

    item_model.name = item.name
    item_model.price = item.price
    item_model.brand = item.brand

    db.add(item_model)
    db.commit()

    return item


@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_model = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()

    if item_model is None:
        raise HTTPException(
            status_code=404,
            detail="Item ID does not exist."
        )

    db.query(models.Inventory).filter(models.Inventory.id == item_id).delete()

    db.commit()

    return {"Success": "Item deleted."}
