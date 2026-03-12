from flask import Flask, render_template, request, redirect
from datetime import datetime

from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

tasks = []

# Prometheus Metrics
tasks_created = Counter('tasks_created_total', 'Total tasks created')
tasks_completed = Counter('tasks_completed_total', 'Total tasks completed')
tasks_pending = Gauge('tasks_pending_total', 'Pending tasks')

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        tasks.append({
            "task": task,
            "status": "Pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tasks_created.inc()
        tasks_pending.inc()

    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks[task_id]["status"] = "Completed"
    tasks_completed.inc()
    tasks_pending.dec()

    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if tasks[task_id]["status"] == "Pending":
        tasks_pending.dec()

    tasks.pop(task_id)

    return redirect("/")

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
