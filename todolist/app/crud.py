from typing import List, Optional
from ..utils import enum
from sqlalchemy.orm import Session

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


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Todo]:
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def update_todo(db: Session, todo: models.Todo, update: schemas.TodoUpdate) -> models.Todo:
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


