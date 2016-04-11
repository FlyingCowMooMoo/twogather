#Just a playground :D

import re
from config import EMPLOYEE_ICONS_CSS, BASEDIR

def extract_css_classes():
    textfile = open(EMPLOYEE_ICONS_CSS, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall("\.([\w_-]+)", filetext)
    for m in matches:
        print m + '\n'

extract_css_classes()