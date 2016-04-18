import collections
import csv

import datetime
import os
import random

import re

from app import app, db
from flask import render_template, request, jsonify, Response
from peewee import fn, DoesNotExist, IntegrityError

from config import BASEDIR, EMPLOYEE_ICONS_CSS, IMAGE_FOLDER_LOCATION
from dbmodels import Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard, BoardTask \
    , Logo, Color, Comment, TaskComment

import wwwmodels as wm


@app.before_first_request
def prepare():
    refresh_logos()
    # populate_dummy_data()


@app.route('/', methods=['GET'])
def index():
    b = demo_data()
    print b
    return render_template('taskdemo.html', tasks=b[0])


@app.route('/getcomments/<int:taskid>', methods=['POST'])
def get_comments(taskid=None):
    try:
        try:
            taskid = int(taskid)
        except ValueError:
            raise DoesNotExist('Task Id Needs to be numeric')
        if taskid is None:
            raise DoesNotExist('Task Id Needs to be specified')
        comments = (Comment.select().join(TaskComment).where(TaskComment.task.id == taskid))
        data = jsonify(comments=comments)
    except DoesNotExist as e:
        data = jsonify(error='Invalid Task Id ' + e.message)

    return Response(response=data, status=200, mimetype="application/json")




@app.route('/updatepin', methods=['POST'])
def update_pin():
    pin = request.form['pin']
    color = request.form['color']
    logo = request.form['logo']
    try:
        e = EmployeePin.select(EmployeePin.color.hex_color == color, EmployeePin.logo.logo_class == logo)
        data = jsonify(error='Invalid Color/Logo Combination, already claimed by another employee')
        return Response(response=data, status=200, mimetype="application/json")
    except DoesNotExist:
        try:
            emp = EmployeePin.select(EmployeePin.pin == pin)
            if emp is None:
                raise DoesNotExist
            lg = Logo.select(Logo.logo_class == logo).first()
            cl = Color.select(Color.hex_code == color).first()
            if lg is None or cl is None:
                data = jsonify(error='Invalid Color/Logo Combination')
                return Response(response=data, status=200, mimetype="application/json")
            emp.color = color
            emp.logo = logo
            emp.save()
        except DoesNotExist:
            data = jsonify(error='Invalid employee id')
            return Response(response=data, status=200, mimetype="application/json")


@app.route('/marktask', methods=['POST'])
def updatetask():
    pin = request.form['pin']

    try:
        brd = int(request.form['board'])
    except ValueError:
        data = jsonify(error='Invalid Board Id')
        return Response(response=data, status=200, mimetype="application/json")

    try:
        tsk = int(request.form['task'])
    except ValueError:
        data = jsonify(error='Invalid Task Id')
        return Response(response=data, status=200, mimetype="application/json")

    try:
        task = Task.select(Task.id == brd)
    except DoesNotExist:
        data = jsonify(error='Invalid Task Id')
        return Response(response=data, status=200, mimetype="application/json")

    try:
        board = TaskBoard.select(TaskBoard.id == brd)
    except DoesNotExist:
        data = jsonify(error='Invalid Board Id')
        return Response(response=data, status=200, mimetype="application/json")

    try:
        employee = EmployeePin.select(EmployeePin.pin == pin)
    except DoesNotExist:
        data = jsonify(error='Invalid Employee Pin')
        return Response(response=data, status=200, mimetype="application/json")

    taskaction = request.form['action']
    if taskaction == 'markastodo':
        try:
            mm = MarkedAsTodo.select(MarkedAsTodo.task == task)
            data = jsonify(error='Task is already masked as ToDo')
            return Response(response=data, status=200, mimetype="application/json")
        except DoesNotExist:
            mmm = MarkedAsTodo()
            mmm.task = task
            mmm.employee = employee
            mmm.save()
            data = jsonify(markedastodo=mmm.get_id)
            return Response(response=data, status=200, mimetype="application/json")

    elif taskaction == 'markasdone':
        print('a')
        # TODO: Handle marked as done


'''

@app.route('/board/<string:boardname>', methods=['GET'])
def show_board(boardname):
    board = TaskBoard.get(TaskBoard.name == boardname)
    if board is None:
        return render_template('error.html'), 404
    tasks = BoardTask.select(BoardTask.board == board)
    tasktodo = BoardTask.select(BoardTask.board == board, BoardTask.task.marked_as_todo == True)
    done = BoardTask.select(BoardTask.board == board, BoardTask.task.marked_as_completed == True)
    result = wm.Board(title=board.title, managername=board.creator.name)
    for t in tasks:
        tsk = t.task
        title = tsk.title
        desc = tsk.description

        if tsk.marked_as_task:# wt = tsk.
        ftsk = wm.Task(title=title, desc=desc)
    return render_template('board.html', thetasks=tasks, theboard=board)
'''


def populate_dummy_data():
    Role.drop_table(True)
    User.drop_table(True)
    UserRoles.drop_table(True)
    Task.drop_table(True)
    TaskCompletion.drop_table(True)
    MarkedAsTodo.drop_table(True)
    TaskBoard.drop_table(True)
    BoardTask.drop_table(True)
    EmployeePin.drop_table(True)
    db.database.create_tables([Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard,
                               BoardTask], True)
    with open(os.path.join(BASEDIR, 'dummypins.csv')) as g:
        for pin in g.readlines():
            entry = EmployeePin()
            entry.pin = str(pin.rstrip())
            entry.save()

    reader = csv.reader(open(os.path.join(BASEDIR, 'dummymanagerdata.csv'), mode='r'))
    manager_role = Role()
    manager_role.name = "Warehouse Manager"
    manager_role.description = "Manager of this warehouse"
    manager_role.save()
    for line in reader:
        manager = User()
        manager.email = line[0].rstrip()
        manager.password = line[1].rstrip()
        manager.confirmed_at = datetime.datetime.now()
        manager.name = line[2].rstrip()
        manager.save()
        their_role = UserRoles()
        their_role.user = manager
        their_role.role = manager_role
        their_role.save()
        taskboard = TaskBoard()
        taskboard.creator = manager
        taskboard.name = ''.join((manager.name, '\'s board'))
        taskboard.created_at = datetime.datetime.now()
        taskboard.save()
        reader2 = csv.reader(open(os.path.join(BASEDIR, 'dummytasks.csv'), mode='r'))
        for line2 in reader2:
            task = Task()
            task.title = line[0].rstrip()
            task.description = line[1].rstrip()
            task.save()
            bt = BoardTask()
            bt.board = taskboard
            bt.task = task
            bt.save()


def refresh_color():
    db.database.create_tables([Color], True)
    with open(os.path.join(BASEDIR, 'dummycolors.csv')) as g:
        stuff = g.readlines()
    if stuff is not None:
        for line in stuff:
            value = line.rstrip()
            try:
                Color.select(Color.hex_code == value)
            except DoesNotExist:
                c = Color()
                c.hex_code = value
                c.save()


def refresh_logos():
    db.database.create_tables([Logo], True)
    css_file = open(EMPLOYEE_ICONS_CSS, 'r')
    css_text = css_file.read()
    css_file.close()
    matches = re.findall("\.([\w_-]+)", css_text)
    for m in matches:
        logo = Logo()
        logo.logo_class = m.rstrip()
        try:
            logo.save()
        except IntegrityError as ie:
            print ie.message


def demo_data():
    boards = list()
    employees = get_dummy_employees()
    manager_names = get_dummy_manager_names()
    dummy_tasks = get_dummy_tasks()
    for _ in range(5):
        boards.append(get_dummy_board(tasks=dummy_tasks, manager=random.choice(manager_names), employees=employees))
    return tuple(boards)


def get_dummy_board(tasks=None, manager=None, employees=None):
    if not (not (manager is None) and not (tasks is None) and not (employees is None) and isinstance(manager,
                                                                                                     collections.Iterable) and isinstance( employees, collections.Iterable)):
        raise ValueError('Invalid parameters')
    actions = ['unassigned', 'todo', 'done']
    btasks = list()
    name = 'Board ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    counter = 0
    for t in tasks:
        emp = random.choice(employees)
        bt = wm.Task(id=counter, title=t[0], desc=t[1], logo_class=emp.logo, priority=None, pin=emp.pin, color=emp.color,
                     urgent=random.choice([True, False]), startdate=None, updatedate=None)
        action = random.choice(actions)
        if action == 'unassigned':
            bt.unassigned = True
        elif action == 'todo':
            bt.unassigned = False
            bt.todo = True
        else:
            bt.unassigned = False
            bt.done = True
        btasks.append(bt)
        counter += 1
    return tuple(btasks)


def get_dummy_employees():
    employee_pins = get_dummy_employee_pins()
    icons = get_dummy_icons()
    colors = get_dummy_colors()
    number_of_employees = min(len(employee_pins), len(icons))
    icons_to_use = random.sample(icons, number_of_employees)
    pins_to_use = random.sample(employee_pins, number_of_employees)
    colors_to_use = random.sample(colors, number_of_employees)
    employees = list()
    index = 0
    for p in pins_to_use:
        emp = wm.Employee(pin=p, logo=icons_to_use[index], color=colors_to_use[index])
        index += 1
        employees.append(emp)
    return tuple(employees)


def get_dummy_employee_pins():
    data = list()
    with open(os.path.join(BASEDIR, 'dummypins.csv')) as g:
        for pin in g.readlines():
            data.append(str(pin.rstrip()))
        g.close()
    return tuple(data)


def get_dummy_colors():
    data = list()
    with open(os.path.join(BASEDIR, 'dummycolors.csv')) as g:
        for pin in g.readlines():
            data.append(str(pin.rstrip()))
        g.close()
    return tuple(data)


def get_dummy_manager_names():
    data = list()
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummymanagerdata.csv'), mode='r'))
    for line in reader:
        name = line[2].rstrip()
        data.append(name)
    return tuple(data)


def get_dummy_icons():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(IMAGE_FOLDER_LOCATION) if isfile(join(IMAGE_FOLDER_LOCATION, f))]
    return tuple(onlyfiles)
    '''
    data = list()
    css_file = open(EMPLOYEE_ICONS_CSS, 'r')
    css_text = css_file.read()
    css_file.close()
    matches = re.findall("\.([\w_-]+)", css_text)
    for m in matches:
        data.append(str(m.rstrip()))
    return tuple(data)
    '''


def get_dummy_tasks():
    data = list()
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummytasks.csv'), mode='r'))
    counter = 0
    for line in reader:
        title = str(line[0].rstrip())
        desc = str(line[1].rstrip())
        data.append(tuple([title, desc]))
        counter += 1
    return data
