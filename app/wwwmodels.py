# The Models that hold data to pass to the rendering engine


class Board():
    def __init__(self, tasks=(), todo=(), done=(), title='', managername=''):
        self.tasks = tasks
        self.todo = todo
        self.done = done
        self.title = title
        self.managername = managername


class Task():
    def __init__(self, title='', desc='', logo_class='', priority='', pin='', color='', urgent=False, startdate=None,
                 updatedate=None):
        self.title = title
        self.desc = desc
        self.pin = pin
        self.color = color
        self.logo_class = logo_class
        self.priority = priority
        self.urgent = urgent
        self.startdate = startdate
        self.updatedate = updatedate
