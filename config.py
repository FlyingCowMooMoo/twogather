import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = {
    'name': 'demba.db',
    'engine': 'peewee.SqliteDatabase',
}

