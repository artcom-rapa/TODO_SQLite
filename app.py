from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from collections import namedtuple
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
            print(data)
            projects.create_project(data)
            return render_template('showData.html', form=todoformproject)
        if todoformtask.validate_on_submit():
            data = tuple(todoformtask.data.values())[:5]
            tasks.create_task(data)
            return render_template('showData.html', form1=todoformtask)

    return render_template('index.html', form1=todoformtask, form=todoformproject, projects=projects.all_projects())


@app.route("/task/<int:task_id>/", methods=["GET", "POST"])
def task_details(task_id):
    task = tasks.get_tasks(task_id)

    Task = namedtuple("Task", ["project_id", "task_title", "description", "start_date_t", "end_date_t"])

    start_date = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S')

    ta = Task(
        project_id=task[1],
        task_title=task[2],
        description=task[3],
        start_date_t=start_date,
        end_date_t=end_date
    )

    form1 = TodoFormTask(obj=ta)

    if request.method == "POST":
        if form1.validate_on_submit():
            form1 = TodoFormTask(obj=ta)
            print(tuple(form1.data.values())[:5])
            tasks.update(task_id, tuple(form1.data.values())[:5])
            return render_template('showData.html', form1=form1)
    return render_template("task.html", form1=form1, task_id=task_id, task=task)


@app.route("/tasks/", methods=["GET", "POST"])
def tasks_list():
    todoformtask = TodoFormTask()

    if request.method == "POST":
        data = tuple(todoformtask.data.values())
        tasks.creat_task(data)
        return render_template('showData.html', form1=todoformtask)
    return render_template("tasks.html", tasks=tasks.all_tasks(), form1=todoformtask)


@app.route("/projects/", methods=["GET", "POST"])
def projects_list():
    todoformproject = TodoFormProject()

    if request.method == "POST":
        if todoformproject.validate_on_submit():
            return redirect(url_for("index"))
    return render_template("projects.html", projects=projects.all_projects(), form=todoformproject)


@app.route("/project/<int:project_id>/", methods=["GET", "POST"])
def project_details(project_id):
    project = projects.get_projects(project_id)
    tasks = projects.get_tasks(project_id)

    Project = namedtuple("Project", ["project_title", "start_date_p", "end_date_p", "done"])

    start_date = datetime.strptime(project[2], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(project[3], '%Y-%m-%d %H:%M:%S')

    pr = Project(
        project_title=project[1],
        start_date_p=start_date,
        end_date_p=end_date,
        done=project[4],
    )

    form = TodoFormProject(obj=pr)
    form1 = TodoFormTask()

    if request.method == "POST":
        if form.validate_on_submit():
            form = TodoFormProject(obj=pr)
            projects.update(project_id, tuple(form.data.values())[:4])
            return render_template('showData.html', form=form)
        if form1.validate_on_submit():
            print(form1.data.values())
            data = tuple(form1.data.values())[:5]
            tasks.create_task(data)
            return render_template('showData.html', form1=form1)
    return render_template("project.html", form=form, form1=form1, tasks=tasks, project=project, project_id=project_id)


if __name__ == "__main__":
    app.run(debug=True)
