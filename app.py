from flask import Flask, jsonify, request, render_template, redirect, url_for
from models import Task

app = Flask(__name__)

tasks = {}
task_id_counter = 1

@app.route("/")
def home():
    return render_template("home.html", tasks=tasks.values())

@app.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html')

@app.route("/add_task", methods=["POST"])
def add_task():
    global task_id_counter
    title = request.form.get("title")
    description = request.form.get("description")
    
    if not title:
        return "Title is required", 400

    new_task = Task(task_id=task_id_counter, title=title, description=description)
    tasks[task_id_counter] = new_task
    task_id_counter += 1

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

