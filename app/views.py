import dbutils

from app import app, db
from flask import render_template, request, jsonify, Response
from peewee import fn, DoesNotExist

from dbmodels import TaskBoard, Comment, TaskComment, BoardTask, Task

import wwwmodels as viewmodels


@app.before_first_request
def prepare():
    dbutils.verify_tables(drop_tables=True, generate_data=True)


@app.route('/', methods=['GET'])
def index():
    items = list()
    for item in tuple(TaskBoard.select()):
        items.append(item.id)
    return render_template('index.html', items=tuple(items))


@app.route('/showboard/<int:board_id>', methods=['GET'])
def show_board(board_id=None):
    if board_id is None:
        return show_error('400', 'No board id specified')
    try:
        board = TaskBoard.get(TaskBoard.id == board_id)
        query = tuple(Task.select().join(BoardTask).join(TaskBoard).where(TaskBoard.id == board_id))
        tasks = list()
        for item in query:
            tasks.append(viewmodels.Task.create_from_dbmodel(item))
        return render_template('taskdemo.html', tasks=tuple(tasks))
    except DoesNotExist as e:
        show_error('404', e.message)

@app.route('/getcomments', methods=['POST'])
def get_comments():
    taskid = request.get_json()['task_id']
    print taskid
    try:
        try:
            taskid = int(taskid)
        except ValueError:
            raise DoesNotExist('Task Id Needs to be numeric')
        if taskid is None:
            raise DoesNotExist('Task Id Needs to be specified')
        comments = (Comment.select().join(TaskComment).where(TaskComment.task == taskid))

        data = jsonify(comments=comments)
    except DoesNotExist as e:
        data = jsonify(error='Invalid Task Id ' + e.message)

    return Response(response=data, status=200, mimetype="application/json")


def show_error(code=None, msg=None):
    return render_template('error.html', code=code, msg = msg)