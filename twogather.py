#!flask/bin/python
from app import app

import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

app.run(debug=True)


