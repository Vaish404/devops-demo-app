from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

tasks = []
tasks_created = 0
tasks_completed = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global tasks_created
    if request.method == "POST":
        task_name = request.form.get("task")
        task = {
            "name": task_name,
            "status": "Pending",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(task)
        tasks_created += 1
        return redirect("/")
    return render_template("index.html", tasks=tasks)


@app.route("/complete/<int:index>")
def complete(index):
    global tasks_completed
    if 0 <= index < len(tasks):
        tasks[index]["status"] = "Completed"
        tasks_completed += 1
    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return redirect("/")


@app.route("/health")
def health():
    return {"status": "Application Running"}


@app.route("/metrics")
def metrics():
    return f"""
tasks_created_total {tasks_created}
tasks_completed_total {tasks_completed}
tasks_pending_total {len(tasks) - tasks_completed}
"""
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
