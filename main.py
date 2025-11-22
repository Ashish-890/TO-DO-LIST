from datetime import datetime, date

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoRead

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Static files + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------
# HOME / INBOX / TODAY / UPCOMING / PROJECT VIEWS
# ---------------------------------------------------------
@app.get("/")
def read_home(
    request: Request,
    q: str | None = None,
    priority_filter: str | None = None,
    project: str = "Inbox",
    db: Session = Depends(get_db),
):
    """
    Inbox     -> ALL tasks
    Today     -> tasks due today   (from all projects)
    Upcoming  -> tasks due in future (from all projects)
    Projects  -> only tasks of that project
    """

    today = date.today()

    # -------- FILTER BY VIEW TYPE --------
    if project == "Inbox":
        base_query = db.query(Todo)

    elif project == "Today":
        base_query = db.query(Todo).filter(Todo.due_date == today)

    elif project == "Upcoming":
        base_query = db.query(Todo).filter(Todo.due_date > today)

    else:
        # For real projects (Education, Gym, My work, Side project etc.)
        base_query = db.query(Todo).filter(Todo.project == project)

    query = base_query

    # -------- SEARCH FILTER --------
    if q:
        query = query.filter(Todo.title.ilike(f"%{q}%"))

    # -------- PRIORITY FILTER --------
    if priority_filter and priority_filter != "all":
        query = query.filter(Todo.priority == priority_filter)

    # -------- SORTING: dated → undated → newest --------
    todos = query.order_by(
        Todo.due_date.is_(None),
        Todo.due_date,
        Todo.id.desc()
    ).all()

    # -------- STATISTICS --------
    total = base_query.count()
    completed = base_query.filter(Todo.is_done == True).count()  # noqa
    pending = total - completed
    high_priority_pending = (
        base_query
        .filter(Todo.priority == "high", Todo.is_done == False)
        .count()
    )

    stats = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority_pending": high_priority_pending,
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
            "q": q or "",
            "priority_filter": priority_filter or "all",
            "project": project,
            "stats": stats,
        },
    )


# ---------------------------------------------------------
# ADD TODO
# ---------------------------------------------------------
@app.post("/add")
def add_todo(
    title: str = Form(...),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    project: str = Form("Inbox"),
    db: Session = Depends(get_db),
):
    parsed_due_date = None
    if due_date:
        parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

    todo = Todo(
        title=title,
        priority=priority,
        due_date=parsed_due_date,
        project=project,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return RedirectResponse(url=f"/?project={project}", status_code=303)


# ---------------------------------------------------------
# TOGGLE COMPLETE
# ---------------------------------------------------------
@app.post("/toggle/{todo_id}")
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    project = "Inbox"
    if todo:
        todo.is_done = not todo.is_done
        project = todo.project
        db.commit()
    return RedirectResponse(url=f"/?project={project}", status_code=303)


# ---------------------------------------------------------
# DELETE TODO
# ---------------------------------------------------------
@app.post("/delete/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    project = todo.project if todo else "Inbox"
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url=f"/?project={project}", status_code=303)


# ---------------------------------------------------------
# EDIT TODO (PAGE)
# ---------------------------------------------------------
@app.get("/edit/{todo_id}")
def edit_page(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "todo": todo},
    )


# ---------------------------------------------------------
# EDIT TODO (SUBMIT)
# ---------------------------------------------------------
@app.post("/edit/{todo_id}")
def edit_todo(
    todo_id: int,
    title: str = Form(...),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    project: str = Form("Inbox"),
    db: Session = Depends(get_db),
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return RedirectResponse(url="/", status_code=303)

    todo.title = title
    todo.priority = priority
    todo.project = project

    if due_date:
        todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    else:
        todo.due_date = None

    db.commit()
    db.refresh(todo)
    return RedirectResponse(url=f"/?project={todo.project}", status_code=303)


# ---------------------------------------------------------
# JSON API (OPTIONAL / FOR FUTURE)
# ---------------------------------------------------------
@app.get("/api/todos", response_model=list[TodoRead])
def api_get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return todos


@app.post("/api/todos", response_model=TodoRead)
def api_create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(
        title=todo_in.title,
        priority=todo_in.priority,
        due_date=todo_in.due_date,
        project=todo_in.project,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.patch("/api/todos/{todo_id}", response_model=TodoRead)
def api_update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return RedirectResponse(url="/", status_code=404)

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.priority is not None:
        todo.priority = todo_update.priority
    if todo_update.due_date is not None:
        todo.due_date = todo_update.due_date
    if todo_update.is_done is not None:
        todo.is_done = todo_update.is_done
    if todo_update.project is not None:
        todo.project = todo_update.project

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}")
def api_delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return {"message": "Deleted"}
