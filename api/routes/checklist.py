from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Checklist, CheklistItems
from api.routes import auth


router = APIRouter(
    prefix="/checklist",
    tags=["checklist"]
)

class CreateChecklistRequest(BaseModel):
    name: str

class CreateChecklistItemRequest(BaseModel):
    itemName: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_checklist(create_checklist_request: CreateChecklistRequest, db: db_dependency, user: user_dependency):
    create_checklist_model = Checklist(
        name=create_checklist_request.name,
        user_id=user["user_id"]
    )
    db.add(create_checklist_model)
    db.commit()

@router.get("/", status_code=status.HTTP_200_OK)
async def list_checklist(db: db_dependency, user: user_dependency):
    list = db.query(Checklist).filter(Checklist.user_id == user["user_id"]).all()
    return {"checklist": list}

@router.delete("/{checklist_id}", status_code=status.HTTP_200_OK)
async def delete_checklist(checklist_id: int, db: db_dependency, user: user_dependency):
    db.query(Checklist).filter(Checklist.id == checklist_id, Checklist.user_id == user["user_id"]).delete()
    db.commit()

@router.post("/{checklist_id}/item", status_code=status.HTTP_201_CREATED)
async def create_checklist_item(
    checklist_id: int,
    create_checklist_item_request: CreateChecklistItemRequest,
    db: db_dependency,
    user: user_dependency):
    create_checklist_item_model = CheklistItems(
        itemName=create_checklist_item_request.itemName,
        checklist_id=checklist_id
    )
    db.add(create_checklist_item_model)
    db.commit()

@router.get("/{checklist_id}/item", status_code=status.HTTP_200_OK)
async def list_checklist_item(checklist_id: int, db: db_dependency, user: user_dependency):
    list = db.query(CheklistItems).filter(CheklistItems.checklist_id == checklist_id).all()
    return {"checklist_items": list}

@router.get("/{checklist_id}/item/{item_id}", status_code=status.HTTP_200_OK)
async def get_checklist_item(checklist_id: int, item_id: int, db: db_dependency, user: user_dependency):
    item = db.query(CheklistItems).filter(CheklistItems.id == item_id, CheklistItems.checklist_id == checklist_id).first()
    return {"checklist_item": item}

@router.put("/{checklist_id}/item/{item_id}", status_code=status.HTTP_200_OK)
async def update_status_checklist_item(checklist_id: int, item_id: int, db: db_dependency, user: user_dependency):
    current_status = db.query(CheklistItems).filter(CheklistItems.id == item_id, CheklistItems.checklist_id == checklist_id).first().status
    db.query(CheklistItems).filter(CheklistItems.id == item_id, CheklistItems.checklist_id == checklist_id).update({"status": not current_status})
    db.commit()

@router.put("/{checklist_id}/item/{item_id}/rename", status_code=status.HTTP_200_OK)
async def rename_checklist_item(checklist_id: int, item_id: int, checklist_item_rename: CreateChecklistItemRequest, db: db_dependency, user: user_dependency):
    db.query(CheklistItems).filter(CheklistItems.id == item_id, CheklistItems.checklist_id == checklist_id).update({"itemName": checklist_item_rename.itemName})
    db.commit()

@router.delete("/{checklist_id}/item/{item_id}", status_code=status.HTTP_200_OK)
async def delete_checklist_item(checklist_id: int, item_id: int, db: db_dependency, user: user_dependency):
    db.query(CheklistItems).filter(CheklistItems.id == item_id, CheklistItems.checklist_id == checklist_id).delete()
    db.commit()
