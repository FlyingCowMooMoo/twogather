import datetime

from flask.ext.security import UserMixin, RoleMixin

from flask_peewee.db import CharField, TextField, BooleanField, DateTimeField, ForeignKeyField, PrimaryKeyField

from app import db


class Organization(db.Model):
    id = PrimaryKeyField()
    name = TextField(unique=True)


class LogoImage(db.Model):
    id = PrimaryKeyField()
    image_name = TextField()


class Color(db.Model):
    id = PrimaryKeyField()
    hex_code = TextField(unique=True)


class Role(db.Model, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)


class User(db.Model, UserMixin):
    id = PrimaryKeyField()
    email = TextField(unique=True)
    password = TextField(null=True)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)
    name = TextField(null=True)

    def get_name(self):
        if self.name is None:
            return self.email
        else:
            return self.name



class UserRoles(db.Model):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)


class EmployeePin(db.Model):
    pin = TextField(unique=True)
    logo = ForeignKeyField(LogoImage, null=True)
    color = ForeignKeyField(Color, null=True)
    email = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    organization = ForeignKeyField(Organization)
    hex_color = property(lambda self: self.color.hex_code)
    logo_url = property(lambda self: self.logo.image_name)

    def get_abv(self):
        if self.first_name is not None and self.last_name is not None:
            fn = str(self.first_name)
            ln = str(self.last_name)
            return ''.join((fn[0:1], ln[0:1]))
        else:
            return 'N/A'


class Task(db.Model):
    id = PrimaryKeyField()
    title = TextField(null=False)
    description = TextField(null=True)
    marked_as_task = BooleanField(default=True)
    marked_as_todo = BooleanField(default=False)
    marked_as_completed = BooleanField(default=False)
    assigned_at = DateTimeField(null=False, default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    completed_at = DateTimeField(null=True)
    marked_by = ForeignKeyField(EmployeePin, null=True)
    marked_as_high_priority = BooleanField(default=False)


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
    organization = ForeignKeyField(Organization)
    org_id = property(lambda self: self.organization.id)
    org_name = property(lambda self: self.organization.name)


class BoardTask(db.Model):
    id = PrimaryKeyField()
    board = ForeignKeyField(TaskBoard)
    task = ForeignKeyField(Task)


class Comment(db.Model):
    id = PrimaryKeyField()
    text = TextField()
    date = DateTimeField(null=False, default=datetime.datetime.now)
    created_by_employee = ForeignKeyField(EmployeePin, null=True, default=None)
    created_by_manager = ForeignKeyField(User, null=True, default=None)

    def get_author(self):
        if self.created_by_employee is not None:
            if self.created_by_employee.first_name is not None and self.created_by_employee.last_name is not None:
                return ' '.join((self.created_by_employee.first_name, self.created_by_employee.last_name))
            else:
                return str(self.created_by_employee.pin)
        elif self.created_by_manager is not None:
            if self.created_by_manager.name is not None:
                return self.created_by_manager.name
            else:
                return self.created_by_manager.email
        else:
            return 'Unnamed Author'


class TaskComment(db.Model):
    task = ForeignKeyField(Task, null=False)
    comment = ForeignKeyField(Comment, null=False)
    taskid = property(lambda self: self.task.id)
