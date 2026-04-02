from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API", description="Manage a simple ToDo list.")

_todos: dict[int, dict] = {}
_next_id: int = 1


class TodoCreate(BaseModel):
    content: str = Field(..., min_length=1)


class TodoUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None


class Todo(BaseModel):
    todo_id: int
    content: str
    completed: bool = False


def _get_todo_or_404(todo_id: int) -> dict:
    if todo_id not in _todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return _todos[todo_id]


@app.get("/")
async def root():
    return {"message": "Todo API", "docs": "/docs"}


@app.get("/todos", response_model=list[Todo])
async def list_todos():
    return sorted(_todos.values(), key=lambda t: t["todo_id"])


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(payload: TodoCreate):
    global _next_id
    tid = _next_id
    _next_id += 1
    row = {"todo_id": tid, "content": payload.content, "completed": False}
    _todos[tid] = row
    return row


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    return _get_todo_or_404(todo_id)


@app.patch("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, payload: TodoUpdate):
    row = _get_todo_or_404(todo_id)
    if payload.content is not None:
        row["content"] = payload.content
    if payload.completed is not None:
        row["completed"] = payload.completed
    return row


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    _get_todo_or_404(todo_id)
    del _todos[todo_id]
