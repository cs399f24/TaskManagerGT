from flask import Flask, jsonify, request
from models import Task

app = Flask(__name__)

# In-memory database for tasks (will reset each time the app restarts)
tasks = {}
task_id_counter = 1

@app.route("/")
def home():
    return jsonify({"message": "Welcome to TaskManagerGT!"})

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks.values()])

# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = Task(task_id=task_id_counter, title=title, description=description)
    tasks[task_id_counter] = new_task
    task_id_counter += 1
    
    return jsonify(new_task.to_dict()), 201

# Update an existing task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    
    return jsonify(task.to_dict())

# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404
    
    del tasks[task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


