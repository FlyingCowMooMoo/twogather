import dbutils

from app import app, db
from flask import render_template, request, jsonify, Response
from peewee import fn, DoesNotExist

from dbmodels import TaskBoard, Comment, TaskComment, BoardTask, Task, EmployeePin, User, Organization

import wwwmodels as viewmodels

import utils


@app.before_first_request
def prepare():
    # dbutils.verify_tables(drop_tables=True, generate_data=True)
    print ('a')


@app.route('/', methods=['GET'])
def index():
    items = list()
    for item in tuple(TaskBoard.select()):
        items.append(item.id)
    return render_template('index.html', items=tuple(items))


@app.route('/showboard/<int:board_id>', methods=['GET'])
def show_board(board_id=None):
    if board_id is None:
        return show_error('400', 'No board id specified')
    try:
        board = TaskBoard.get(TaskBoard.id == board_id)
        query = tuple(Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id))
        tasks = list()
        for item in query:
            tasks.append(viewmodels.Task.create_from_dbmodel(item))
        return render_template('taskdemo.html', tasks=tuple(tasks))
    except DoesNotExist as e:
        return show_error('404', e.message)


@app.route('/companies')
def companies():
    return render_template('companies.html', items=tuple(Organization.select()))


@app.route('/company/<int:cid>')
def company(cid=None):
    if cid is None:
        return show_error('404', 'Page not found')
    else:
        try:
            org = Organization.get(Organization.id == cid)
            boards = tuple(TaskBoard.select().where(TaskBoard.organization == org))
        except DoesNotExist:
            return show_error('404', 'Page not found')
        data = list()
        for b in boards:
            data.append({'id': b.id, 'name': b.name})
        return render_template('boards.html', items=tuple(data))



@app.route('/createtask', methods=['GET'])
def create_task():
    employees = list()
    boards = list()
    managers = list()
    for value in TaskBoard.select():
        boards.append({'id': value.id, 'name': value.name})
    for value in EmployeePin.select():
        if value.first_name and value.last_name:
            name = ' '.join((value.first_name, value.last_name))
        else:
            name = 'No name specified'
        employees.append({'pin': value.pin, 'color': value.color.hex_code, 'image': value.logo.image_name, 'name': name})
    for value in User.select():
        managers.append({'id': value.id, 'name': value.name})
    return render_template('createtask.html', employees=tuple(employees), boards=tuple(boards),
                           managers=tuple(managers))


@app.route('/tasks/<int:id>')
def task_details():
    try:
        task = Task.get(Task.id == id)
    except DoesNotExist:
        return show_error('404', 'Could not find this task')


@app.route('/submitcreatetask', methods=['POST'])
def submit_create_task():
    try:
        board_id = int(request.form['board_id'])
        task_title = request.form['task_title']
        task_desc = request.form['task_desc']
        if request.form['employee_id'] != 'NONE':
            employee_id = int(request.form['employee_id'])
        manager_id = int(request.form['manager_id'])
        urgent = utils.to_bool(request.form['urgent'])
    except ValueError as ve:
        return jsonify(error="Invalid Parameters", details=ve.message)
    if board_id is None or task_title is None or task_desc is None or manager_id is None:
        return jsonify(error="Invalid Parameters")
    try:
        assign_to_employee = False
        board = TaskBoard.get(TaskBoard.id == board_id)
        if employee_id != 'NONE':
            assign_to_employee = True
            employee = EmployeePin.get(EmployeePin.pin == employee_id)
        manager = User.get(User.id == manager_id)
        task = Task()
        task.title = task_title
        task.description = task_desc
        task.marked_as_high_priority = urgent
        if assign_to_employee:
            task.marked_by = employee
        task.save()
        bt = BoardTask()
        bt.task = task
        bt.board = board
        bt.save()
    except DoesNotExist:
        return jsonify(error="Invalid Parameters")


@app.route('/getcomments', methods=['POST'])
def get_comments():
    datac = list()
    taskid = int(request.json['task_id'])
    print taskid
    try:
        try:
            taskid = int(taskid)
        except ValueError:
            raise DoesNotExist('Task Id Needs to be numeric')
        if taskid is None:
            raise DoesNotExist('Task Id Needs to be specified')
        # for tc in TaskComment.select():
        #    if tc.taskid == taskid:
        #        datac.append(tc.comment)

        for c in Comment.select().join(TaskComment).where(TaskComment.task == taskid):
            author = c.get_author()
            datac.append({'author': c.get_author(), 'text': c.text})
        # comments = (Comment.select().join(TaskComment).where(TaskComment.task == taskid))

        return jsonify(comments=datac)
    except DoesNotExist as e:
        return jsonify(error='Invalid Task Id ' + e.message)

    return Response(response=data, status=200, mimetype="application/json")


def show_error(code=None, msg=None):
    return render_template('error.html', code=code, msg=msg)
