# app/api/v1/users.py
from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["用户"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的详细信息。
    """
    return current_user