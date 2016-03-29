import csv
import datetime
import logging

from flask import Flask
from flask.ext.peewee.db import Database
from flask.ext.security import PeeweeUserDatastore, Security

app = Flask(__name__)
app.config.from_object('config')
db = Database(app)

from app.dbmodels import Role, User, UserRoles

user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

from app import views
