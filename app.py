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
            data = tuple(todoformproject.data.values())[:4]
            projects.create_project(data)
            return render_template('showData.html', form=todoformproject)
        if todoformtask.validate_on_submit():
            data = tuple(todoformtask.data.values())[:5]
            tasks.create_task(data)
            return render_template('showData.html', form1=todoformtask)

    return render_template('index.html', form1=todoformtask, form=todoformproject, projects=projects.all_projects())


@app.route("/tasks/<int:task_id>/", methods=["GET", "POST"])
def task_details(task_id):
    task = tasks.get_tasks(task_id)
    task_dict = {
        "project_id": task[1],
        "name": task[2],
        "descriptions": task[3],
        "start_date": task[4],
        "end_date": task[5]
    }

    form1 = TodoFormTask(data=task_dict)

    if request.method == "POST":
        if form1.validate_on_submit():
            print(tuple(form1.data.values())[:5])
            data = task_id, tuple(form1.data.values())[:5]
            tasks.update(data)
            return render_template('showData.html', form1=form1)
    return render_template("task.html", form=form1, task_id=task_id, task=task)


@app.route("/tasks/", methods=["GET", "POST"])
def tasks_list():
    todoformtask = TodoFormTask()

    if request.method == "POST":
        data = tuple(todoformtask.data.values())
        tasks.update(data)
        return render_template('showData.html', form1=todoformtask)
    return render_template("tasks.html", tasks=tasks.all_tasks(), form1=todoformtask)


@app.route("/projects/", methods=["GET", "POST"])
def projects_list():
    todoformproject = TodoFormProject()

    if request.method == "POST":
        if todoformproject.validate_on_submit():
            return redirect(url_for("index"))
    return render_template("projects.html", projects=projects.all_projects(), form=todoformproject)


@app.route("/projects/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get_projects(project_id)
    tasks = projects.get_tasks(project_id)
    print(tasks)

    project_dict = {
        "name": project[1],
        "start_date": project[2],
        "end_date": project[3],
        "done": project[4],
    }

    form = TodoFormProject(data=project_dict)
    form1 = TodoFormTask()

    if request.method == "POST":
        if form.validate_on_submit():
            print(tuple(form1.data.values())[:4])
            data = project_id, tuple(form1.data.values())[:4]
            project.update(data)
            return render_template('showData.html', form=form)
        if form1.validate_on_submit():
            print(form1.data.values())
            data = tuple(form1.data.values())[:5]
            tasks.create_task(data)
            return render_template('showData.html', form1=form1)
    return render_template("project.html", form=form, form1=form1, project=project, tasks=tasks, project_id=project_id)


if __name__ == "__main__":
    app.run(debug=True)
