from flask import Flask, request, render_template, redirect, url_for

from TODO_SQLite.forms import TodoFormProject, TodoFormTask
from TODO_SQLite.models import projects, tasks

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/", methods=["GET", "POST"])
def index():
    todoformproject = TodoFormProject()
    todoformtask = TodoFormTask()

    if request.method == "POST":

        if todoformproject.validate_on_submit():
            print(todoformproject.data.values())
            data = tuple(todoformproject.data.values())[:4]
            projects.create_project(data)
            return redirect(url_for("index"))

        if todoformtask.validate_on_submit():
            print(todoformtask.data.values())
            data = tuple(todoformtask.data.values())[:5]
            tasks.create_task(data)
            return render_template('showData.html', form1=todoformtask)

    return render_template('index.html', form1=todoformtask, form=todoformproject, projects=projects.all_projects())


@app.route("/projects/", methods=["GET"])
def projects_list():
    return render_template("projects.html", projects=projects.all_projects())


@app.route("/projects/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get_projects(project_id)

    project_dict = {
        "name": project[1],
        "start_date": project[2],
        "end_date": project[3],
        "status": project[4]
    }

    form = TodoFormProject(data=project_dict)

    if request.method == "POST":
        if form.validate_on_submit():
            projects.update(project_id, tuple(form.data.values())[:4])
        return redirect(url_for("projects_list"))
    return render_template("project.html", form=form, project=project, project_id=project_id)


"""
@app.route("/todos/<int:project_id>/<int:task_id>/", methods=["GET", "POST"])
def task_details(project_id, task_id):
    task = tasks.get_tasks(task_id)

    task_dict = {
        "project_id": tasks[1],
        "name": tasks[2],
        "descriptions": tasks[3],
        "start_date": tasks[4],
        "end_date": tasks[5],
    }
    form = TodoFormTask(data=task_dict)

    if request.method == "POST":
        print(form.data.values())
        if form.validate_on_submit():
            tasks.update(task_id, tuple(form.data.values())[:5])
        return redirect(url_for("projects_list"))
    return render_template("todo_task.html", form=form, task=task, project_id=project_id,
                           task_id=task_id)
"""

if __name__ == "__main__":
    app.run(debug=True)
