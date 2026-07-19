from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.task import (
    create_task, get_tasks_with_filter, get_task, update_task, delete_task
)
from app.schemas.task import TaskCreate, TaskUpdate, TaskQueryParams, PaginatedResponse, TaskResponse
from app.models.task import Task

class TaskService:
    @staticmethod
    def create(db: Session, user_id: int, task_in: TaskCreate) -> Task:
        return create_task(db, user_id, task_in)

    @staticmethod
    def list_tasks(db: Session, user_id: int, query_params: TaskQueryParams) -> PaginatedResponse:
        tasks, total = get_tasks_with_filter(db, user_id, query_params)
        return PaginatedResponse(
            total=total,
            page=query_params.page,
            page_size=query_params.page_size,
            items=[TaskResponse.model_validate(t) for t in tasks]
        )

    @staticmethod
    def get(db: Session, task_id: int, user_id: int) -> Task:
        task = get_task(db, task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        return task

    @staticmethod
    def update(db: Session, task_id: int, user_id: int, task_in: TaskUpdate) -> Task:
        task = get_task(db, task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        return update_task(db, task, task_in)

    @staticmethod
    def delete(db: Session, task_id: int, user_id: int):
        task = get_task(db, task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")
        delete_task(db, task)