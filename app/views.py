import csv

import datetime
import os

from app import app, db
from flask import render_template
from peewee import fn, IntegrityError

from config import BASEDIR
from dbmodels import Task
from dbmodels import Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo


@app.before_first_request
def prepare():
    Role.drop_table(True)
    User.drop_table(True)
    UserRoles.drop_table(True)
    EmployeePin.drop_table(True)
    Task.drop_table(True)
    TaskCompletion.drop_table(True)
    MarkedAsTodo.drop_table(True)
    db.database.create_tables([Role, User, UserRoles, EmployeePin, Task, TaskCompletion, MarkedAsTodo], True)
    with open(os.path.join(BASEDIR, 'dummypins.csv')) as g:
        for pin in g.readlines():
            entry = EmployeePin()
            entry.pin = str(pin.rstrip())
            entry.save()

    reader = csv.reader(open(os.path.join(BASEDIR, 'dummymanagerdata.csv'), mode='r'))
    for line in reader:
        manager = User()
        manager.email = line[0].rstrip()
        manager.password = line[1].rstrip()
        manager.confirmed_at = datetime.datetime.now()
        manager.save()
    reader = csv.reader(open(os.path.join(BASEDIR, 'dummytasks.csv'), mode='r'))
    for line in reader:
        task = Task()
        task.title = line[0].rstrip()
        task.description = line[1].rstrip()
        task.save()

        # else:


@app.route('/', methods=['GET'])
def index():
    print 'lol'
    tasks = Task.select().order_by(fn.Random())
    return render_template('tasks.html', thetasks=tasks)
