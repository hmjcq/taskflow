from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

# ---------- 请求体 ----------
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: int = Field(0, ge=0, le=5)          # 假设优先级 0~5
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=0, le=5)
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None

# ---------- 响应体 ----------
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: int
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- 分页响应 ----------
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[TaskResponse]

# ---------- 查询参数 ----------
class TaskQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    keyword: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    category_id: Optional[int] = None
    sort: Optional[str] = Field(None, pattern=r"^(created_at|priority|due_date|status)$")  # 允许的排序字段