from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from database_models import User
from schemas.user_schema import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


# Get all Users
@router.get("/", response_model= List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    query = db.query(User)
    users = query.all()

    if not users:
        raise HTTPException(status_code=404, detail= "No users found")
    return users


# Get a user by ID
@router.get("/{user_id}", response_model= UserResponse, summary= "Get a User by ID")
def get_user_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Create a new User
@router.post("/", response_model= UserResponse, summary= "Create a User")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role.value,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Update user data
@router.put("/{user_id}", response_model= UserResponse, summary= "Update a User")
def update_user(user_id: int, updated_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_data.username != user.username and db.query(User).filter(User.username == updated_data.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if updated_data.email != user.email and db.query(User).filter(User.email == updated_data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    
    user.username = updated_data.username
    user.email = updated_data.email
    user.password = updated_data.password
    user.role = updated_data.role.value

    db.commit()
    db.refresh(user)
    return user


# Delete a user
@router.delete("/{user_id}", summary= "Delete a User")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail= "User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
