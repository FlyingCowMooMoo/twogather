import datetime

from flask.ext.security import UserMixin, RoleMixin

from flask_peewee.db import CharField, TextField, BooleanField, DateTimeField, ForeignKeyField, DecimalField, \
    IntegerField, DateField, PrimaryKeyField

from app import db

class Role(db.Model, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)


class User(db.Model, UserMixin):
    email = TextField(unique=True)
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)
    name = TextField()


class UserRoles(db.Model):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)


class EmployeePin(db.Model):
    pin = TextField(unique=True)


class Task(db.Model):
    id = PrimaryKeyField()
    title = TextField()
    description = TextField()
    marked_as_task = BooleanField(default=True)
    marked_as_todo = BooleanField(default=False)
    marked_as_completed = BooleanField(default=False)
    assigned_at = DateTimeField(null=False, default=datetime.datetime.now)
    completed_at = DateTimeField(null=True)


class TaskCompletion(db.Model):
    task = ForeignKeyField(Task)
    employee = ForeignKeyField(EmployeePin)


class MarkedAsTodo(db.Model):
    task = ForeignKeyField(Task)
    employee = ForeignKeyField(EmployeePin)
    marked_at = DateTimeField(null=False, default=datetime.datetime.now)


class TaskBoard(db.Model):
    id = PrimaryKeyField()
    name = TextField(unique=True)
    creator = ForeignKeyField(User)
    created_at = DateTimeField(null=False, default=datetime.datetime.now)


class BoardTask(db.Model):
    id = PrimaryKeyField()
    board = ForeignKeyField(TaskBoard)
    task = ForeignKeyField(Task)


class Logo(db.Model):
    id = PrimaryKeyField()
    logo_class = TextField(unique=True)


class Shift(db.Model):
    id = PrimaryKeyField()
    day = DateTimeField(null=False, default=datetime.datetime.now, unique=True)


class EmployeeShift(db.Model):
    id = PrimaryKeyField()
    employee = ForeignKeyField(EmployeePin)
    shift = ForeignKeyField(Shift)
    color = TextField(null=False)
    logo = ForeignKeyField(Logo)
