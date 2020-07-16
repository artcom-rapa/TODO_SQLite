from flask import Flask, request, render_template, redirect, url_for

from forms import TodoFormProject
from forms import TodoFormTask
from models import projects
from models import tasks

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/todos/", methods=["GET", "POST"])
def projects_list():
    form = TodoFormProject()
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            projects.create_project(form.data)
        return redirect(url_for("projects_list"))

    return render_template("todos.html", form=form, projects=projects.all_projects(), error=error)


@app.route("/todos/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get(project_id - 1)
    form = TodoFormProject(data=project)

    if request.method == "POST":
        if form.validate_on_submit():
            projects.update(project_id - 1, form.data)
        return redirect(url_for("project_list"))
    return render_template("todo.html", form=form, project_id=project_id)


def tasks_list():
    form = TodoFormTask()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            tasks.create_task(form.data)
        return redirect(url_for("tasks_list"))

    return render_template("todo.html", form=form, tasks=tasks.all_tasks(), error=error)


if __name__ == "__main__":
    app.run(debug=True)
