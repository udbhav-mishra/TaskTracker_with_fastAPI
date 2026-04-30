from fastapi import FastAPI, HTTPException
import datetime
import json
import os

app = FastAPI()

FILE = "task.json"
status = ["pending", "in_progress", "done"]


def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        try:
            return json.loads(content)
        except:
            return []

def save(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)


@app.get("/")
def home():
    return {"message": "Task Tracker API running"}

# CREATE
@app.post("/tasks")
def add_task(description: str):
    tasks = load()
    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "description": description,
        "status": status[0],
        "created_at": datetime.datetime.now().isoformat()
    }
    tasks.append(new_task)
    save(tasks)
    return {"message": "Task added", "task": new_task}

# READ
@app.get("/tasks")
def list_tasks(filter_status: str = None):
    tasks = load()
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    return tasks

# UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, description: str):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["description"] = description
            t["updated_at"] = datetime.datetime.now().isoformat()
            save(tasks)
            return {"message": "Task updated", "task": t}
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(tasks) == len(new_tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    save(new_tasks)
    return {"message": "Task deleted"}

# MARK IN PROGRESS
@app.patch("/tasks/{task_id}/in-progress")
def mark_in_progress(task_id: int):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status[1]
            save(tasks)
            return {"message": "Marked in progress"}
    raise HTTPException(status_code=404, detail="Task not found")

# MARK DONE
@app.patch("/tasks/{task_id}/done")
def mark_done(task_id: int):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status[2]
            save(tasks)
            return {"message": "Marked as done"}
    raise HTTPException(status_code=404, detail="Task not found")