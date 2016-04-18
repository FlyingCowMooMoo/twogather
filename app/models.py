import datetime

from flask.ext.security import UserMixin, RoleMixin

from flask_peewee.db import CharField, TextField, BooleanField, DateTimeField, ForeignKeyField, PrimaryKeyField

from app import db


class LogoImage(db.Model):
    id = PrimaryKeyField()
    image_name = TextField(unique=True)


class Color(db.Model):
    id = PrimaryKeyField()
    hex_code = TextField(unique=True)


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
    logo = ForeignKeyField(LogoImage, null=True, unique=True)
    color = ForeignKeyField(Color, null=True, unique=True)