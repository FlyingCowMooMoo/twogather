import json
import random
import string

import datetime
from flask.ext.login import login_required, current_user, login_user, logout_user
from playhouse.migrate import SqliteMigrator, migrate

import dbutils

from app import app, db
from flask import render_template, request, jsonify, Response, url_for, redirect
from peewee import fn, DoesNotExist, TextField, BooleanField, ForeignKeyField

from dbmodels import TaskBoard, Comment, TaskComment, BoardTask, Task, EmployeePin, User, Organization, Color

import wwwmodels as viewmodels

import utils


@app.before_first_request
def prepare():
    # dbutils.new_random_boards()
    # dbutils.verify_tables(drop_tables=True, generate_data=True)
    # m = SqliteMigrator(db.database)
    # migrate(m.add_column('task', 'hidden', BooleanField(default=False)))
    # migrate(m.add_column('user', 'organization_id', ForeignKeyField(Organization, null=True, to_field=Organization.id)))
    # migrate(m.add_column('taskboard', 'hidden', BooleanField(default=False)))
    # for u in User.select():
    #   org = (Organization.select().order_by(fn.Random())).get()
    #  u.organization = org
    # u.save()
    # for t in Task.select():
    #    if t.marked_as_completed and t.completed_at is None:
    #        t.completed_at = dbutils.random_date(t.assigned_at, datetime.datetime.now())
    #        t.save()

    print ('a')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('signin'))


@app.route('/editboard', methods=['POST'])
def edit_board():
    bid = int(request.json['id'])
    title = request.json['title']
    desc = request.json['desc']
    try:
        board = TaskBoard.get(TaskBoard.id == bid)
    except DoesNotExist as e:
        return jsonify(error='An error has occurred ' + e.message)
    try:
        board.name = title
        board.description = desc
        board.save()
        return jsonify(msg='Board has been updated')
    except Exception as e:
        return jsonify(error='An error has occurred ' + e.message)


@app.route('/togglevisibility', methods=['POST'])
def toggle_visibility():
    task = int(request.json['task'])
    try:
        t = Task.get(Task.id == task)
        if t.hidden:
            t.hidden = False
            msg = 'Task has been restored'
        else:
            t.hidden = True
            msg = 'Task has been deleted'
        t.save()
        return jsonify(msg=msg)
    except DoesNotExist:
        return jsonify(error='Invalid Task')
    except Exception as e:
        return jsonify(error='An error has occurred ' + e.message)

@app.route('/toggleboardvisibility', methods=['POST'])
def toggle_board_visibility():
    b = int(request.json['board'])
    try:
        t = TaskBoard.get(TaskBoard.id == b)
        if t.hidden:
            t.hidden = False
            msg = 'Board has been restored'
        else:
            t.hidden = True
            msg = 'Board has been deleted'
        t.save()
        return jsonify(msg=msg)
    except DoesNotExist:
        return jsonify(error='Invalid Board')
    except Exception as e:
        return jsonify(error='An error has occurred ' + e.message)


@app.route('/toggleurgency', methods=['POST'])
def toggle_urgency():
    task = int(request.json['task'])
    try:
        t = Task.get(Task.id == task)
        if t.marked_as_high_priority:
            t.marked_as_high_priority = False
            msg = 'Task has been unmarked as urgent'
        else:
            t.marked_as_high_priority = True
            msg = 'Task has been marked as urgent'
        t.save()
        return jsonify(msg=msg)
    except DoesNotExist:
        return jsonify(error='Invalid Task')
    except Exception as e:
        return jsonify(error='An error has occurred ' + e.message)


@app.route('/assigntask', methods=['POST'])
def assign_task():
    emp_id = request.json['emp']
    print request.json
    task_id = int(request.json['task'])
    try:
        emp = EmployeePin.get(EmployeePin.pin == emp_id)
    except DoesNotExist:
        return jsonify(error='Invalid Employee')
    try:
        task = Task.get(Task.id == task_id)
    except DoesNotExist:
        return jsonify(error='Invalid Employee')
    try:
        task.marked_by = emp
        task.save()
        return jsonify(msg='Task has been assigned to ' + emp.first_name + " " + emp.last_name)
    except Exception as e:
        return jsonify(error='An error has occurred ' + e.message)


@app.route('/createemployee', methods=['POST'])
def create_employee():
    fn = request.json['first-name']
    ln = request.json['last-name']
    color = request.json['color']
    org = int(request.json['org'])
    try:
        org = Organization.get(Organization.id == org)
    except:
        return jsonify(error='Invalid Warehouse')

    valid_pin = False
    pin = ''
    while not valid_pin:
        pin = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        try:
            EmployeePin.get(EmployeePin.pin == pin)
        except DoesNotExist:
            valid_pin = True
    try:
        try:
            c = Color.get(Color.hex_code == color)
        except:
            c = Color()
            c.hex_code = color
            c.save()
            color = Color.get(Color.hex_code == color)

        emp = EmployeePin()
        emp.pin = pin
        emp.color = color
        emp.first_name = fn
        emp.last_name = ln
        emp.organization = org
        emp.save()
        emp = {"id": emp.id, "color": emp.hex_color, "pin": emp.pin,
               "fname": emp.first_name, "lname": emp.last_name}
        return jsonify(employee=emp)
    except Exception as e:
        return jsonify(error='An error occurred.Details: ' + e.message)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('pages/login.html')
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        try:
            user = User.get(User.email == email)
        except DoesNotExist:
            return jsonify(error='Invalid Credentials')
        if user.password == password:
            login_user(user)
            return jsonify(id=user.id, name=user.name, url=url_for('company', cid=user.organization.id))
        else:
            return jsonify(error='Invalid Credentials')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('pages/signup.html')
    if request.method == 'POST':
        cm = request.json['company']
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        query = User.select().where(User.email == email)
        if query.exists():
            return jsonify(error='Email already in use')
        query = Organization.select().where(Organization.name == cm)
        if query.exists():
            return jsonify(error='A warehouse already exists with the specified name')

        manager = User()
        manager.email = email
        manager.name = name
        manager.password = password
        manager.save()

        c = Organization()
        c.name = cm
        c.save()

        manager = User.get(User.email == email)
        c = Organization.get(Organization.name == cm)

        manager.organization = c
        manager.save()

        return jsonify(msg='You have successfully signed up', url=url_for('company', cid=c.id))

    return jsonify(error='Invalid Credentials')


@app.route('/showboard/<int:board_id>', methods=['GET'])
@login_required
def show_board(board_id=None):
    if board_id is None:
        return show_error('400', 'No board id specified')
    try:
        board = TaskBoard.get(TaskBoard.id == board_id)
        return render_template('pages/board.html', id=board_id, orgid=board.org_id,
                               orgname=board.org_name, accountname=current_user.name, managerid=current_user.id,
                               boardname=board.name)
    except DoesNotExist as e:
        return show_error('404', e.message)


@app.route('/logs/<int:board_id>', methods=['GET'])
@login_required
def logs(board_id):
    if board_id is None:
        return show_error('400', 'No board id specified')
    try:
        board = TaskBoard.get(TaskBoard.id == board_id)
        cid = board.org_id
        data = list()
        for task in Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id):
            data.append({"event": 'Task created. ' + task.title, "date": task.assigned_at})
            if Task.completed_at is not None:
                data.append({"event": 'Task completed. ' + task.title + " marked as completed by " + task.get_worker(),
                             "date": task.assigned_at})
        data.sort(key=lambda r: r.get("date"))
        return render_template('pages/logs.html', id=board_id,
                               orgid=board.org_id,
                               orgname=board.org_name, accountname=current_user.name, managerid=current_user.id,
                               boardname=board.name, bid=board.id, items=tuple(data), cid=cid)
    except DoesNotExist as e:
        return show_error('404', e.message)


@app.route('/report/<int:board_id>', methods=['GET'])
@login_required
def report(board_id):
    if board_id is None:
        return show_error('400', 'No board id specified')
    try:
        board = TaskBoard.get(TaskBoard.id == board_id)
        cid = board.org_id
        try:
            t = Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id,
                                                                    Task.marked_as_task).count()
        except DoesNotExist:
            t = 0
        try:
            td = Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id,
                                                                     Task.marked_as_todo).count()
        except DoesNotExist:
            td = 0
        try:
            d = Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id,
                                                                    Task.marked_as_completed).count()
        except DoesNotExist:
            d = 0

        start_date = datetime.date.today() - datetime.timedelta(days=30)
        end_date = datetime.date.today()
        data = list()
        for today in utils.daterange(start_date, end_date):
            try:
                assigned = Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id,
                                                                               Task.assigned_at.between(
                                                                                   today - datetime.timedelta(days=1),
                                                                                   today)).count()
            except DoesNotExist:
                assigned = 0

            try:
                completed = Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id,
                                                                                Task.completed_at.between(
                                                                                    today - datetime.timedelta(days=1),
                                                                                    today)).count()
            except DoesNotExist:
                completed = 0
            data.append({"date": today, "assigned": assigned, "completed": completed})
        return render_template('pages/report.html', total=t + td + d, t=t, td=td, d=d, id=board_id,
                               orgid=board.org_id,
                               orgname=board.org_name, accountname=current_user.name, managerid=current_user.id,
                               boardname=board.name, bid=board.id, lastdays=tuple(data), cid=cid)
    except DoesNotExist as e:
        return show_error('404', e.message)


@app.route('/gettasks', methods=['POST'])
def get_tasks():
    board_id = int(request.json['board_id'])
    board = TaskBoard.get(TaskBoard.id == board_id)
    query = tuple(Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id))
    tasks = list()
    for item in query:
        if not item.hidden:
            tasks.append(viewmodels.Task.create_from_dbmodel(item, dbutils.get_comments(item.id)).to_dict())
    return jsonify(tasks=tasks)


@app.route('/hidetask', methods=['POST'])
def hide_task():
    task = request.json['task_id']
    try:
        task = Task.get(Task.id == task)
        return jsonify(msg='All good')
    except DoesNotExist as e:
        return jsonify(error='An error occurred ' + e.message)


@app.route('/addcomment', methods=['POST'])
def add_comment():
    task = request.json['task_id']
    text = request.json['text']
    author_type = request.json['author_type']
    author_id = request.json['author_id']
    try:
        task = Task.get(Task.id == task)
        c = Comment()
        c.text = text
        if author_type == 'manager':
            a = User.get(User.id == author_id)
            c.created_by_manager = a
        else:
            a = EmployeePin.get(EmployeePin.pin == author_id)
            c.created_by_employee = a
        c.save()
        tc = TaskComment()
        tc.comment = c
        tc.task = task
        tc.save()
        return jsonify(msg='Created a new comment')
    except DoesNotExist as e:
        return jsonify(error='An error occurred ' + e.message)


@app.route('/getemployee', methods=['POST'])
def get_employee():
    if request.json['pin'] is None:
        return jsonify(error='Invalid Pin')
    pin = request.json['pin']
    try:
        emp = EmployeePin.get(EmployeePin.pin == pin)
        emp = {"id": emp.id, "color": emp.hex_color, "pin": emp.pin,
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
        task.marked_as_completed = datetime.datetime.now()
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
            employees.append({"id": emp.id, "color": emp.hex_color, "pin": emp.pin,
                              "fname": emp.first_name, "lname": emp.last_name})
        # return Response(response=jsonify(employees=employees), status=200, mimetype="application/json")
        return jsonify(employees=employees)
    except DoesNotExist as e:
        return jsonify(error="Invalid Parameters" + e.message)


@app.route('/getemployeesforboard', methods=['POST'])
def get_employees_for_board():
    bid = int(request.json['board_id'])
    employees = list()
    try:
        for task in Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == bid):
            if task.marked_by is not None:
                emp = task.marked_by
                employees.append({"id": emp.id, "color": emp.hex_color, "pin": emp.pin,
                                  "fname": emp.first_name, "lname": emp.last_name})
        employees = map(dict, set(tuple(sorted(d.items())) for d in employees))
        return jsonify(employees=employees)
    except DoesNotExist as e:
        return jsonify(error="Invalid Parameters" + e.message)


@app.route('/companies')
def companies():
    return render_template('companies.html', items=tuple(Organization.select()))


@app.route('/company/<int:cid>')
@login_required
def company(cid=None):
    print(current_user.email)
    if cid is None:
        return show_error('404', 'Page not found')
    else:
        try:
            org = Organization.get(Organization.id == cid)
            return render_template('pages/boards.html', id=org.id, name=current_user.name, mid=current_user.id,
                                   orgname=org.name)
        except DoesNotExist:
            return show_error('404', 'Page not found')


@app.route('/createboard', methods=['POST'])
def create_board():
    orgid = int(request.json['org_id'])
    title = request.json['title']
    desc = request.json['desc']
    manager = int(request.json['manager'])

    try:
        manager = User.get(User.id == manager)
        org = Organization.get(Organization.id == orgid)
    except DoesNotExist:
        return jsonify(error='Invalid Manager Id')

    board = TaskBoard()
    board.creator = manager
    board.name = title
    board.description = desc
    board.organization = org
    try:
        board.save()
        b = {'id': board.id, 'name': board.name, 'desc': board.description, 'count': 0}
        return jsonify(msg='Successfully created a board with title: ' + board.name, board=b)
    except Exception as e:
        return jsonify(error=e.message)


@app.route('/getboards', methods=['POST'])
def get_boards():
    orgid = int(request.json['org_id'])
    try:
        org = Organization.get(Organization.id == orgid)
        boards = tuple(TaskBoard.select().where(TaskBoard.organization == org, TaskBoard.hidden == False))
    except DoesNotExist:
        return jsonify(error="Invalid Board Id")
    data = list()
    for b in boards:
        count = 0
        for a in BoardTask.select():
            if a.board_id == b.id:
                count += 1
        ta = list()
        for task in Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == b.id):
            if task.marked_by is not None:
                ta.append(task.emp_id)

        data.append({'id': b.id, 'name': b.name, 'desc': b.description, 'count': count, 'emps': len(list(set(ta)))})
    return jsonify(boards=data)


@app.route('/submitcreatetask', methods=['POST'])
def submit_create_task():
    a = request.json
    try:
        board_id = int(request.json['board_id'])
        task_title = request.json['task_title']
        task_desc = request.json['task_desc']
        if request.json['employee_id'] != 'none':
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
        if request.json['employee_id'] != 'none':
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


def show_error(code=None, msg=None):
    return render_template('error.html', code=code, msg=msg)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('signin'))
