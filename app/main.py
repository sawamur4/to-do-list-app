from fastapi import FastAPI, status, Depends, HTTPException
from api.routes import auth
from api.routes import checklist
import models
from database import SessionLocal, engine
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()
app.include_router(auth.router)
app.include_router(checklist.router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(auth.get_current_user)]


@app.get("/user", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User": user}