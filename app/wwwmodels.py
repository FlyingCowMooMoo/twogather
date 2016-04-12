# The Models that hold data to pass to the rendering engine


class Board():
    def __init__(self, tasks=(), todo=(), done=(), title='', managername=''):
        self.tasks = tasks
        self.todo = todo
        self.done = done
        self.title = title
        self.managername = managername


class Task():
    def __init__(self, title=None, desc=None, logo_class=None, priority=None, pin=None, color=None, urgent=False, startdate=None,
                 updatedate=None, unassigned=True, todo=False, done=False):
        self.title = title
        self.desc = desc
        self.pin = pin
        self.color = color
        self.logo_class = logo_class
        self.priority = priority
        self.urgent = urgent
        self.startdate = startdate
        self.updatedate = updatedate


class Employee():
    def __init__(self, pin=None, color=None, logo=None):
        if pin is None:
            raise ValueError('Pin cannot be none')
        if color is None:
            raise ValueError('Color cannot be none')
        if logo is None:
            raise ValueError('Logo cannot be none')
        self.pin = pin
        self.color = color
        self.logo = logo

    def pin(self):
        return self.pin

    def color(self):
        return self.color

    def logo(self):
        return self.logo
