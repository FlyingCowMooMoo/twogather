#Just a playground :D

import re
from config import EMPLOYEE_ICONS_CSS, BASEDIR, IMAGE_FOLDER_LOCATION


def extract_css_classes():
    textfile = open(EMPLOYEE_ICONS_CSS, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall("\.([\w_-]+)", filetext)
    for m in matches:
        print m + '\n'


def extract_icon_names():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(IMAGE_FOLDER_LOCATION) if isfile(join(IMAGE_FOLDER_LOCATION, f))]
    print onlyfiles

#extract_css_classes()

extract_icon_names()