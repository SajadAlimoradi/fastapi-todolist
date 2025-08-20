from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas
from ..utils import enum
from .database import Base, engine, get_db


# Create tables on startup (for simple projects without migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TodoList API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])  # Simple health check
def health():
    return {"status": "ok"}


@app.post(
    "/todos",
    response_model=schemas.TodoOut,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"],
)
def create_todo(todo_in: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo_in)


@app.get(
    "/todos",
    response_model=List[schemas.TodoOut],
    tags=["todos"],
)
def list_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priorities: Optional[List[enum.PriorityEnum]] = None,
    categories: Optional[List[enum.CategoryEnum]] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_todos(
        db,
        skip=skip,
        limit=limit,
        completed=completed,
        priorities=priorities,
        categories=categories,
        q=q,
    )


@app.get("/todos/{todo_id}", response_model=schemas.TodoOut, tags=["todos"])
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch(
    "/todos/{todo_id}",
    response_model=schemas.TodoOut,
    tags=["todos"],
)
def patch_todo(
    todo_id: int,
    update: schemas.TodoUpdate,
    db: Session = Depends(get_db),
):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return crud.update_todo(db, todo, update)


@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["todos"],
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db, todo)
    return
