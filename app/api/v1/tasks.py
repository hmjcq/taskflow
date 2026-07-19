from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskQueryParams, PaginatedResponse
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["任务"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService.create(db, current_user.id, task_in)

@router.get("/", response_model=PaginatedResponse)
def list_tasks(
    params: TaskQueryParams = Depends(),  # 自动解析查询参数
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService.list_tasks(db, current_user.id, params)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService.get(db, task_id, current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TaskService.update(db, task_id, current_user.id, task_in)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    TaskService.delete(db, task_id, current_user.id)