import datetime

from flask.ext.security import UserMixin, RoleMixin

from flask_peewee.db import CharField, TextField, BooleanField, DateTimeField, ForeignKeyField, DecimalField, \
    IntegerField

from peewee import Model, SqliteDatabase

from app import db


class Role(db.Model, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)


class User(db.Model, UserMixin):
    email = TextField(unique=True)
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)


class UserRoles(db.Model):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)


class EmployeePin(db.Model):
    pin = TextField(unique=True)


class Task(db.Model):
    id = IntegerField(primary_key=True)
    title = TextField()
    description = TextField()
    completed = BooleanField(default=False)
    assigned_at = DateTimeField(null=False, default=datetime.datetime.now())
    completed_at = DateTimeField(null=True)


class TaskCompletion(db.Model):
    task = ForeignKeyField(Task)
    employee = ForeignKeyField(EmployeePin)


class MarkedAsTodo(db.Model):
    task = ForeignKeyField(Task)
    employee = ForeignKeyField(EmployeePin)
    marked_at = DateTimeField(null=False, default=datetime.datetime.now())
