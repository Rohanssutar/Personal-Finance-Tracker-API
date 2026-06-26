from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from database_models import User
from schemas.user_schema import UserCreate, UserResponse
from security import hash_password
from dependencies import required_roles


router = APIRouter(prefix="/users", tags=["Users"])


# Get all Users — admin only
@router.get("/", response_model=List[UserResponse], summary="Get All Users", description="Accessible by Admins only.")
def get_all_users(
    db: Session = Depends(get_db),
    user: User = Depends(required_roles(["admin"]))
):
    query = db.query(User)
    users = query.all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
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
        password=hash_password(user.password),
        role=user.role.value,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Update user data — admin only
@router.put("/{user_id}", response_model=UserResponse, summary="Update a User", description="Accessible by Admins only.")
def update_user(
    user_id: int,
    updated_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(required_roles(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if updated_data.username != user.username and db.query(User).filter(User.username == updated_data.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if updated_data.email != user.email and db.query(User).filter(User.email == updated_data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    
    user.username = updated_data.username
    user.email = updated_data.email
    user.password = hash_password(updated_data.password)
    user.role = updated_data.role.value

    db.commit()
    db.refresh(user)
    return user


# Delete a user — admin only
@router.delete("/{user_id}", summary="Delete a User", description="Accessible by Admins only.")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(required_roles(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail= "User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
