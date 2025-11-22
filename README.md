# 📝 TO-DO LIST – FastAPI Productivity App

![FastAPI](https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)


A modern, fully functional task manager built with **FastAPI**, **SQLAlchemy**, **Jinja2**, and **SQLite** — featuring multiple workspaces, priorities, due dates, search filters, and clean UI.

---

## 🚀 Features

### ✅ Task Features
- Create, edit, delete tasks  
- Mark tasks as completed/incomplete  
- Priority levels: Low, Medium, High  
- Due dates with **Today / Upcoming** filters  
- Project-based categorization (Education, Gym, Work, Side project etc.)

### 🔍 Filters & Search
- Filter tasks by priority  
- Search tasks by title  
- View tasks by:
  - **Inbox** – all tasks  
  - **Today** – tasks due today  
  - **Upcoming** – tasks due in future  
  - **Workspace** – specific project  

### 💻 Frontend & UI
- Clean and modern UI  
- Custom CSS  
- Jinja2 templating  
- Fully responsive layout  

### 🗃 Tech Stack
- **FastAPI** – backend  
- **SQLAlchemy** – ORM  
- **SQLite** – database  
- **Jinja2** – templating  
- **HTML + CSS** – UI  

---

## 📂 Project Structure
```bash
📁 TO-DO-LIST
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── edit.html
└── static/
    └── style.css
```

---

## ▶️ Running the App Locally

### 1. Clone repository
```bash
git clone https://github.com/Ashish-890/TO-DO-LIST.git
cd TO-DO-LIST
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the server
```bash
uvicorn main:app --reload
```

### Open in browser:
```
http://127.0.0.1:8000
```

---

## 📌 Future Enhancements
- User login & authentication  
- Light/Dark mode  
- Drag-and-drop task sorting  
- Calendar view  
- Notification reminders  

---

## 📜 License
This project is licensed under the **MIT License**.

