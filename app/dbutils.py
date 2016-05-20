# coding=utf-8
import csv
import random

from peewee import fn, DoesNotExist

from app import db
from config import IMAGE_FOLDER_LOCATION, BASEDIR
from dbmodels import Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard, BoardTask, \
    LogoImage, Color, Comment, TaskComment, Organization

import datetime
from random import randint


def verify_tables(drop_tables=False, generate_data=False):
    if drop_tables:
        Role.drop_table(True)
        User.drop_table(True)
        UserRoles.drop_table(True)
        EmployeePin.drop_table(True)
        Task.drop_table(True)
        TaskCompletion.drop_table(True)
        MarkedAsTodo.drop_table(True)
        TaskBoard.drop_table(True)
        BoardTask.drop_table(True)
        LogoImage.drop_table(True)
        Color.drop_table(True)
        Comment.drop_table(True)
        TaskComment.drop_table(True)
        Organization.drop_table(True)
    db.database.create_tables(
            [Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard, BoardTask, LogoImage,
             Color, Comment, TaskComment, Organization], True)
    populate_logos()
    populate_colors()
    _ = Role.create_or_get(name='Manager')
    if generate_data:
        populate_dummy_companies()
        populate_dummy_managers()
        populate_dummy_employees()
        generate_random_boards()
        populate_dummy_comments()


def new_random_boards():
    Task.drop_table(True)
    TaskBoard.drop_table(True)
    BoardTask.drop_table(True)
    Comment.drop_table(True)
    TaskComment.drop_table(True)
    EmployeePin.drop_table(True)
    db.database.create_tables(
            [Task, TaskBoard, BoardTask, TaskComment, EmployeePin, Comment], True)
    populate_dummy_employees()
    generate_random_boards()
    populate_dummy_comments()


def generate_random_boards(number=5, tasks_per_board=20):
    for org in Organization.select():
        random_manager = tuple(User.select().order_by(fn.Random()).limit(number))
        for _ in range(number):
            manager = random.choice(random_manager)
            board = TaskBoard()
            noun = random.choice((
                "driver", "protocol", "bandwidth", "panel", "microchip", "program", "port", "card", "array", "interface",
                "system",
                "sensor", "firewall", "hard drive", "pixel", "alarm", "feed", "monitor", "application", "transmitter", "bus",
                "circuit", "capacitor", "matrix"))
            board.name = ' '.join(('The ', noun.title(),  ' board'))
            board.creator = manager
            board.organization = org
            board.save()
            for _ in range(tasks_per_board):
                task = generate_dummy_task(org)
                bt = BoardTask()
                bt.board = board
                random_query = Task.select().order_by(fn.Random())
                bt.task = random_query.get()
                bt.save()


def generate_dummy_task(org=None):
    verb = random.choice(('back up', 'bypass', "hack", "override", "compress",
                          "copy", "navigate", "index", "connect", "generate", "quantify", "calculate", "synthesize",
                          "input",
                          "transmit", "program", "reboot", "parse"))
    noun = random.choice((
        "driver", "protocol", "bandwidth", "panel", "microchip", "program", "port", "card", "array", "interface",
        "system",
        "sensor", "firewall", "hard drive", "pixel", "alarm", "feed", "monitor", "application", "transmitter", "bus",
        "circuit", "capacitor", "matrix"))

    title = ' '.join((verb, noun))
    action = random.choice(('unassigned', 'todo', 'done'))

    task = Task()
    task.title = title
    task.description = title
    emp = (EmployeePin.select().where(EmployeePin.organization == org).order_by(fn.Random())).get()
    task.assigned_at = random_date(datetime.date.today() - datetime.timedelta(days=30), datetime.date.today())
    if random.choice([True, False]):
        task.marked_by = emp
    if action == 'unassigned':
        task.marked_as_task = True
    elif action == 'todo':
        task.marked_as_task = False
        task.marked_as_todo = True
        task.marked_by = emp
    else:
        task.marked_as_task = False
        task.marked_as_completed = True
        task.marked_by = emp
        task.completed_at = random_date(task.assigned_at, datetime.date.today())
    task.marked_as_high_priority = random.choice([True, False])
    task.save()
    return task


def populate_dummy_employees():
    data = list()
    import os
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummypins.csv'), mode='r'))
    for line in reader:
        random_query = Color.select().order_by(fn.Random())
        color = random_query.get()
        random_query = Organization.select().order_by(fn.Random())
        org = random_query.get()
        d = {'pin': line[0].rstrip(), 'first_name': line[1].rstrip(), 'last_name': line[2].rstrip(),
             'email': line[3].rstrip(), 'color': color, 'organization': org}
        data.append(d)
    with db.database.atomic():
        EmployeePin.insert_many(data).execute()


def populate_dummy_managers():
    managers = load_dummy_managers()
    for m in managers:
        email = str(m.get('email')).rstrip()
        entry = User.create_or_get(email=email)
        entry = User.get(User.email == email)
        entry.password = str(m.get('password')).rstrip()
        entry.name = str(m.get('name')).rstrip()
        entry.save()
        role = Role.get(Role.name == 'Manager')
        ur = UserRoles()
        ur.user = entry
        ur.role = role
        role.save()


def populate_dummy_comments():
    data = list()
    import os
    with open(os.path.join(BASEDIR, 'dummycomments.csv')) as g:
        for line in g.readlines():
            data.append(line.rstrip())
        g.close()
    for task in Task.select():
        for comment in data:
            assign_to_employee = random.choice([True, False])
            c = Comment()
            c.text = comment
            if assign_to_employee:
                random_query = EmployeePin.select().order_by(fn.Random())
                user = random_query.get()
                c.created_by_employee = user
            else:
                random_query = User.select().order_by(fn.Random())
                user = random_query.get()
                c.created_by_manager = user
            c.save()
            tc = TaskComment()
            tc.task = task
            tc.comment = c
            tc.save()


def populate_colors():
    data = list()
    import os
    with open(os.path.join(BASEDIR, 'dummycolors.csv')) as g:
        for line in g.readlines():
            d = {'hex_code': str(line.rstrip())}
            data.append(d)
        g.close()
    with db.database.atomic():
        Color.insert_many(data).execute()


def populate_logos():
    data = list()
    import os
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummyimages.csv'), mode='r'))
    for line in reader:
        man = {'id': line[0].rstrip(), 'image_name': line[1].rstrip()}
        data.append(man)
    with db.database.atomic():
        LogoImage.insert_many(data).execute()


def populate_dummy_companies():
    data = list()
    import os
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummycompanies.csv'), mode='r'))
    for line in reader:
        man = {'id': line[0].rstrip(), 'name': line[1].rstrip()}
        data.append(man)
    with db.database.atomic():
        Organization.insert_many(data).execute()


def load_icons():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(IMAGE_FOLDER_LOCATION) if isfile(join(IMAGE_FOLDER_LOCATION, f))]
    return tuple(onlyfiles)


def load_dummy_managers():
    data = list()
    import os
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummymanagerdata.csv'), mode='r'))
    for line in reader:
        man = {'email': line[0].rstrip(), 'password': line[1].rstrip(), 'name': line[2].rstrip()}
        data.append(man)
    return tuple(data)


def get_comments(task_id):
    if task_id is None:
        raise ValueError('Invalid Task Id')
    data = list()
    try:
        try:
            taskid = int(task_id)
        except ValueError:
            raise DoesNotExist('Task Id Needs to be numeric')
        if taskid is None:
            raise DoesNotExist('Task Id Needs to be specified')

        for c in Comment.select().join(TaskComment).where(TaskComment.task == taskid):
            data.append({'author': c.get_author(), 'text': c.text})
        return tuple(data)
    except DoesNotExist as e:
        return tuple()


def random_date(start, end):
    return start + datetime.timedelta(
            seconds=randint(0, int((end - start).total_seconds())))