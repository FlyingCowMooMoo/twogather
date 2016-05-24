#!flask/bin/python
from app import app

import logging

from config import BASEDIR

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print BASEDIR
app.secret_key = 'super secret keyasd'
app.run(debug=True)


