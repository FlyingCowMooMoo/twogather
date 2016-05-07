# The Models that hold data to pass to the rendering engine a.k.a View Models

import dbmodels as dbm


class Board():
    def __init__(self, tasks=(), todo=(), done=(), title='', managername='', id=None):
        self.tasks = tasks
        self.todo = todo
        self.done = done
        self.title = title
        self.managername = managername
        self.id = id


class Task():
    def __init__(self, id=None, title=None, desc=None, logo_class=None, priority=None, pin=None, color=None,
                 urgent=False, startdate=None,
                 updatedate=None, unassigned=True, todo=False, done=False, comments=list()):
        self.id = id
        self.title = title
        self.desc = desc
        self.pin = pin
        self.color = color
        self.logo_class = logo_class
        self.priority = priority
        self.urgent = urgent
        self.startdate = startdate
        self.updatedate = updatedate
        self.unassigned = unassigned
        self.todo = todo
        self.done = done
        self.comments = comments

    @staticmethod
    def create_from_dbmodel(dbmodel=None, comments=list()):
        if dbmodel is None or not isinstance(dbmodel, dbm.Task):
            raise ValueError('Invalid parameter')
        if dbmodel.marked_as_task:
            unassigned = True
        else:
            unassigned = False

        if dbmodel.marked_as_todo:
            todo = True
        else:
            todo = False
        if dbmodel.marked_as_completed:
            done = True
        else:
            done = False
        color = None
        logo = None
        pin = None
        if dbmodel.marked_by is not None:
            color = dbmodel.marked_by.color.hex_code
            logo = dbmodel.marked_by.logo.image_name
            pin = dbmodel.marked_by.pin
        return Task(dbmodel.id, dbmodel.title, dbmodel.description, logo, dbmodel.marked_as_high_priority,
                    pin, color, dbmodel.marked_as_high_priority, dbmodel.assigned_at,
                    dbmodel.completed_at, unassigned, todo, done, comments)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'desc': self.desc, 'pin': self.pin, 'color': self.color,
                'logo_class': self.logo_class, 'priority': self.priority, 'urgent': self.urgent,
                'startdate': self.startdate, 'updatedate': self.updatedate, 'unassigned': self.unassigned,
                'todo': self.todo, 'done': self.done, 'comments': self.comments}


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


class Comment:
    def __init__(self, comment=None):
        if comment is None or not isinstance(Comment, dbm.Comment):
            raise ValueError('Invalid Parameter')
        self.id = comment.id
        self.text = comment.text
        self.color = '#f2f2f2'
        if comment.created_by_employee is not None:
            self.author = comment.created_by_employee.pin
            self.color = comment.created_by_employee.color.hex_code
        else:
            self.author = comment.created_by_manager.email
