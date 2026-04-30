from fastapi import FastAPI
from tasks import load, save
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Task Tracker API running"}

@app.post("/tasks")
def add_task(task: dict):
    pass

@app.get("/tasks")
def get_tasks():
    pass

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: dict):
    pass

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    pass

@ap.patch("/tasks/{task_id}/status")
def update_status(task_id: int, status: str):
    pass