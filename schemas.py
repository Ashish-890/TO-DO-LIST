from datetime import date
from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    priority: str = "medium"          # low, medium, high
    due_date: date | None = None      # optional
    project: str = "Inbox"            # default project


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    due_date: date | None = None
    is_done: bool | None = None
    project: str | None = None


class TodoRead(BaseModel):
    id: int
    title: str
    is_done: bool
    priority: str
    due_date: date | None
    project: str

    class Config:
        from_attributes = True   # pydantic v2 replacement for orm_mode
