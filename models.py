from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # low, medium, high
    due_date = Column(Date, nullable=True)       # optional
    project = Column(String, default="Inbox")    # Inbox / Education / My work / etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
