import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

EMPLOYEE_ICONS_CSS = os.path.join(BASEDIR, '/app/static/css/employee-icons.css')

DATABASE = {
    'name': 'demba.db',
    'engine': 'peewee.SqliteDatabase',
}

