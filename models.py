from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Checklist(Base):
    __tablename__ = "checklist"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, index=True)

class CheklistItems(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    itemName = Column(String, index=True)
    status = Column(Boolean, unique=False, default=False)
    checklist_id = Column(Integer, index=True)