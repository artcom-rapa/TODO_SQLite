from flask import Flask, request, render_template, redirect, url_for

from TODO_SQLite.forms import TodoFormProject, TodoFormTask
from TODO_SQLite.models import projects, tasks

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/todos/", methods=["GET", "POST"])
def projects_list():
    form = TodoFormProject()
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            projects.create_project((tuple(form.data.values())[:5]))
        return redirect(url_for("projects_list"))

    return render_template("todos.html", form=form, projects=projects.all_projects(), error=error)


@app.route("/todos/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get_projects(project_id)

    project_dict = {
    "name": project[1] ,
    "start_date": project[2],
    "end_date": project[3],
    "status": project[4]
    }

    form = TodoFormProject(data=project_dict)

    if request.method == "POST":
        if form.validate_on_submit():
            projects.update(project_id, tuple(form.data.values())[:5])
        return redirect(url_for("projects_list"))
    return render_template("todo.html", form=form, project=project, project_id=project_id)


def tasks_list():
    form = TodoFormTask()
    error = ""
    if request.method == "POST" and form == TodoFormTask():
        if form.validate_on_submit():
            tasks.create_task((tuple(form.data.values())[:5]))
        return redirect(url_for("tasks_list"))

    return render_template("todo.html", form=form, tasks=tasks.all_tasks(), error=error)


if __name__ == "__main__":
    app.run(debug=True)
