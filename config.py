import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

EMPLOYEE_ICONS_CSS = os.path.join(BASEDIR, 'app\static\css\employee-icons.css')

IMAGE_FOLDER_LOCATION = os.path.join(BASEDIR, 'app\static\img\\')

DATABASE = {
    'name': 'demba.db',
    'engine': 'peewee.SqliteDatabase',
}

