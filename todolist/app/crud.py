from typing import List, Optional
from ..utils import enum
from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas


def create_todo(db: Session, todo_in: schemas.TodoCreate) -> models.Todo:
    todo = models.Todo(
        title=todo_in.title,
        description=todo_in.description,
        priority=todo_in.priority or enum.PriorityEnum.MEDIUM,
        category=todo_in.category or enum.CategoryEnum.WORK,
        due_date=todo_in.due_date,
        completed=todo_in.completed or False,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priorities: Optional[List[enum.PriorityEnum]] = None,
    categories: Optional[List[enum.CategoryEnum]] = None,
    q: Optional[str] = None,
) -> List[models.Todo]:
    query = db.query(models.Todo)

    if completed is not None:
        query = query.filter(models.Todo.completed == completed)

    if priorities:
        query = query.filter(models.Todo.priority.in_(priorities))

    if categories:
        query = query.filter(models.Todo.category.in_(categories))

    if q:
        like_expr = f"%{q}%"
        query = query.filter(
            or_(
                models.Todo.title.ilike(like_expr),
                models.Todo.description.ilike(like_expr),
            )
        )

    return query.offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def update_todo(
    db: Session,
    todo: models.Todo,
    update: schemas.TodoUpdate,
) -> models.Todo:
    if update.title is not None:
        todo.title = update.title
    if update.description is not None:
        todo.description = update.description
    if update.priority is not None:
        todo.priority = update.priority
    if update.category is not None:
        todo.category = update.category
    if update.completed is not None:
        todo.completed = update.completed
    if update.due_date is not None:
        todo.due_date = update.due_date
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: models.Todo) -> None:
    db.delete(todo)
    db.commit()
