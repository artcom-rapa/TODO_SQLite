from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired


class TodoFormProject(FlaskForm):
    project_id = StringField('Project id', validators=[DataRequired()])
    project_title = StringField('Project title', validators=[DataRequired()])
    start_date_p = DateField('Project Start Date', format='%d/%m/%Y')
    end_date_p = DateField('Project Start Date', format='%d/%m/%Y')
    done = BooleanField('done', default=False)


class TodoFormTask(FlaskForm):
    task_id = StringField('Task id', validators=[DataRequired()])
    project_id = StringField('Project id', validators=[DataRequired()])
    task_title = StringField('Task title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date_t = DateField('Task Start Date', format='%d/%m/%Y')
    end_date_t = DateField('Task Start Date', format='%d/%m/%Y')
