from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskQueryParams
from typing import Optional, Tuple, List

def create_task(db: Session, user_id: int, task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status.value if task_in.status else "TODO",
        priority=task_in.priority,
        due_date=task_in.due_date,
        user_id=user_id,
        category_id=task_in.category_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_with_filter(
    db: Session,
    user_id: int,
    query_params: TaskQueryParams
) -> Tuple[List[Task], int]:
    """
    根据条件分页查询任务，返回 (列表, 总数)
    """
    # 基础查询：只查当前用户的任务
    base_query = db.query(Task).filter(Task.user_id == user_id)

    # 关键字搜索（标题或描述中包含关键词）
    if query_params.keyword:
        keyword = f"%{query_params.keyword}%"
        base_query = base_query.filter(
            or_(
                Task.title.ilike(keyword),
                Task.description.ilike(keyword)
            )
        )

    # 精确过滤
    if query_params.status:
        base_query = base_query.filter(Task.status == query_params.status.value)
    if query_params.priority is not None:
        base_query = base_query.filter(Task.priority == query_params.priority)
    if query_params.category_id is not None:
        base_query = base_query.filter(Task.category_id == query_params.category_id)

    # 获取总数（在排序/分页前）
    total = base_query.count()

    # 排序
    sort_field = query_params.sort
    if sort_field:
        # 允许的排序字段已在 Pydantic 中校验，这里直接使用，防止注入
        order_column = getattr(Task, sort_field)
        if sort_field == "priority":
            # 优先级降序，数值越大越紧急
            base_query = base_query.order_by(order_column.desc())
        elif sort_field == "due_date":
            # 截止日期升序，越早的越前
            base_query = base_query.order_by(order_column.asc())
        else:
            # 默认降序（如 created_at）
            base_query = base_query.order_by(order_column.desc())
    else:
        # 无排序时默认按创建时间降序
        base_query = base_query.order_by(Task.created_at.desc())

    # 分页
    offset = (query_params.page - 1) * query_params.page_size
    tasks = base_query.offset(offset).limit(query_params.page_size).all()
    return tasks, total

def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)
    # 如果 status 是枚举类型，需要取值
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = update_data["status"].value
    for field, value in update_data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()