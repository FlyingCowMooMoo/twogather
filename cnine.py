#!flask/bin/python
from app import app
import os

import logging

from config import BASEDIR

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print BASEDIR
app.secret_key = 'super secret key'
app.run(debug=True, host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))