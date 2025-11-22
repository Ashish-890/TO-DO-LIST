import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------
# 1. Create a permanent folder for the database
#    (not in OneDrive, so it won't break)
# -------------------------------------------------------
DB_FOLDER = os.path.join(os.getenv("LOCALAPPDATA"), "todo_app")
os.makedirs(DB_FOLDER, exist_ok=True)

# -------------------------------------------------------
# 2. SQLite file path
# -------------------------------------------------------
DATABASE_URL = f"sqlite:///{os.path.join(DB_FOLDER, 'todo.db')}"

# -------------------------------------------------------
# 3. Engine & session
# -------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------------------------------
# 4. Base class for models
# -------------------------------------------------------
Base = declarative_base()

# -------------------------------------------------------
# 5. Dependency for FastAPI (this is what main.py imports)
# -------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
