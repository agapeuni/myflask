from flask import Blueprint, render_template, url_for, request, redirect
from kanban import ma, db
from kanban.task_models import Task

bp = Blueprint('kanban', __name__, url_prefix='/kanban')


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'priority', 'contents')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@bp.route('/')
@bp.route('/list')
def _list():
    task_list = Task.query.all()
    data_list = tasks_schema.dump(task_list)

    plan = []
    todo = []
    inPr = []
    done = []

    for data in data_list:
        if data['status'] == 'PLAN':
            plan.append(data)
        elif data['status'] == 'TO-DO':
            todo.append(data)
        elif data['status'] == 'In-Progress':
            inPr.append(data)
        else:
            done.append(data)

    plan.sort(key=lambda r: r['priority'])
    todo.sort(key=lambda r: r['priority'])
    inPr.sort(key=lambda r: r['priority'])
    done.sort(key=lambda r: r['priority'])

    return render_template('kanban.html', planTasks=plan, todoTasks=todo, inPrTasks=inPr, doneTasks=done)


@bp.route('/create', methods=('POST',))
def create():
    priority = request.form['priority']
    contents = request.form['contents']
    task = Task(priority=priority, contents=contents)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('kanban._list'))


@bp.route('/modify/<int:task_id>', methods=('POST',))
def modify(task_id):
    task = Task.query.get_or_404(task_id)
    status = request.form['status']
    task.status = status
    db.session.commit()
    return redirect(url_for('kanban._list'))


@bp.route('/remove/<int:task_id>', methods=('POST',))
def remove(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('kanban._list'))
