import json

from flask.ext.login import login_required, current_user

import dbutils

from app import app, db
from flask import render_template, request, jsonify, Response, url_for
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
        return render_template('pages/board.html', id=board_id, orgid=board.org_id,
                               orgname=board.org_name, accountname='')
    except DoesNotExist as e:
        return show_error('404', e.message)


@app.route('/gettasks', methods=['POST'])
def get_tasks():
    board_id = int(request.json['board_id'])
    board = TaskBoard.get(TaskBoard.id == board_id)
    query = tuple(Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id))
    tasks = list()
    for item in query:
        tasks.append(viewmodels.Task.create_from_dbmodel(item, dbutils.get_comments(item.id)).to_dict())
    return jsonify(tasks=tasks)


@app.route('/getemployee', methods=['POST'])
def get_employee():
    if request.json['pin'] is None:
        return jsonify(error='Invalid Pin')
    pin = request.json['pin']
    try:
        emp = EmployeePin.get(EmployeePin.pin == pin)
        emp = {"id": emp.id, "color": emp.hex_color, "logo": emp.logo_url, "pin": emp.pin,
               "fname": emp.first_name, "lname": emp.last_name}
        return jsonify(employee=emp)
    except DoesNotExist:
        return jsonify(error='Invalid Pin')


@app.route('/marktask', methods=['POST'])
def mark_task():
    action = request.json['action']
    emp = request.json['pin']
    task = request.json['task']

    try:
        task = Task.get(Task.id == task)
    except DoesNotExist:
        return jsonify(error='Invalid Task Id')
    try:
        emp = EmployeePin.get(EmployeePin.pin == emp)
    except DoesNotExist:
        return jsonify(error='Invalid PIN')
    task.marked_by = emp
    if action == 'todo':
        task.marked_as_task = False
        task.marked_as_completed = False
        task.marked_as_todo = True
    if action == 'done':
        task.marked_as_task = False
        task.marked_as_completed = True
        task.marked_as_todo = False
    task.save()
    msg = ' '.join(('Task was marked as', action, 'by employee with PIN', emp.pin))
    return jsonify(msg=msg)



@app.route('/getemployees', methods=['POST'])
def get_employees():
    ordid = int(request.json['org_id'])
    employees = list()
    try:
        org = Organization.get(Organization.id == ordid)
        for emp in EmployeePin.select().where(EmployeePin.organization == org):
            employees.append({"id": emp.id, "color": emp.hex_color, "logo": emp.logo_url, "pin": emp.pin,
                              "fname": emp.first_name, "lname": emp.last_name})
        # return Response(response=jsonify(employees=employees), status=200, mimetype="application/json")
        return jsonify(employees=employees)
    except DoesNotExist as e:
        return jsonify(error="Invalid Parameters" + e.message)


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


@app.route('/createtask/<int:boardid>', methods=['GET'])
def create_task(boardid):
    employees = list()
    boards = list()
    managers = list()
    task_board = TaskBoard.get(TaskBoard.id == boardid)
    boards.append({'id': task_board.id, 'name': task_board.name})
    for value in EmployeePin.select().where(EmployeePin.organization == task_board.organization):
        if value.first_name and value.last_name:
            name = ' '.join((value.first_name, value.last_name))
        else:
            name = 'No name specified'
        employees.append(
                {'pin': value.pin, 'color': value.color.hex_code, 'image': value.logo.image_name, 'name': name})
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
    a = request.json
    try:
        board_id = int(request.json['board_id'])
        task_title = request.json['task_title']
        task_desc = request.json['task_desc']
        if request.json['employee_id'] != 'NONE':
            employee_id = request.json['employee_id']
        manager_id = int(request.json['manager_id'])
        urgent = utils.to_bool(request.json['urgent'])
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
        return jsonify(msg="All Good", url=url_for('show_board', board_id=board_id))
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
