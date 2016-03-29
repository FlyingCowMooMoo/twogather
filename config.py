import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = {
    'name': 'twogather.db',
    'engine': 'peewee.SqliteDatabase',
}

