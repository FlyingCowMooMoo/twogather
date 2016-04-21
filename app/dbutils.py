# coding=utf-8
import csv
import random

from peewee import fn

from app import db
from config import IMAGE_FOLDER_LOCATION, BASEDIR
from dbmodels import Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard, BoardTask, \
    LogoImage, Color


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
    db.database.create_tables(
            [Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo, TaskBoard, BoardTask, LogoImage,
             Color], True)
    for i in load_icons():
        _ = LogoImage.create_or_get(image_name=str(i))
    populate_colors()
    _ = Role.create_or_get(name='Manager')
    if generate_data:
        populate_dummy_managers()
        populate_dummy_employees()
        generate_random_boards()


def generate_random_boards(number=5, tasks_per_board=20):
    # managers = (User.select().join(UserRoles).join(Role).where(UserRoles.role.name == 'Manager')).order_by(
    #    fn.Random()).limit(number)
    # lol = tuple(UserRoles.select(UserRoles.role == Role.get(Role.name == 'Manager')).limit(number))
    lol = tuple(User.select().order_by(fn.Random()).limit(number))
    print lol
    for _ in range(number):
        manager = random.choice(lol)
        board = TaskBoard()
        board.name = ' '.join((manager.name, '\'s board', str(random.sample(xrange(10), 4))))
        board.creator = manager
        board.save()
        for _ in range(tasks_per_board):
            task = generate_dummy_task()
            bt = BoardTask()
            bt.board = board
            random_query = Task.select().order_by(fn.Random())
            bt.task = random_query.get()
            bt.save()


def generate_dummy_task():
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
    emp = (EmployeePin.select().order_by(fn.Random())).get()
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
    task.marked_as_high_priority = random.choice([True, False])
    task.save()
    return task


def populate_dummy_employees():
    data = list()
    import os
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummypins.csv'), mode='r'))
    for line in reader:
        d = {'pin': line[0].rstrip(), 'first_name': line[1].rstrip(), 'last_name': line[2].rstrip(),
             'email': line[3].rstrip()}
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
