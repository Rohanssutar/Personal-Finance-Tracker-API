from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from database_models import User


# Get current user from the database
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Role-based access control function 
def required_roles(allowed_roles: list[str]):
    def role_check(user: User = Depends(get_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access Denied")
        return user
    return role_check