/**
 * Created by pete on 8/05/2016.
 */
var animations = ["fadeIn",
    "fadeInDown",
    "fadeInDownBig",
    "fadeInLeft",
    "fadeInLeftBig",
    "fadeInRight",
    "fadeInRightBig",
    "fadeInUp",
    "fadeInUpBig",
    "flipInX",
    "flipInY",
    "rotateInDownLeft",
    "rotateInDownRight",
    "rotateInUpLeft",
    "rotateInUpRight",
    "rollIn",
    "zoomIn",
    "zoomInDown",
    "zoomInLeft",
    "zoomInRight",
    "zoomInUp",
    "slideInDown",
    "slideInLeft",
    "slideInRight",
    "slideInUp",
    "bounce",
    "flash",
    "pulse",
    "rubberBand",
    "shake",
    "headShake",
    "swing",
    "tada",
    "wobble",
    "jello"
];

function randomAnim()
{
    var r = "fadeInRight";
    return "animated " + r;
}

function alertModal(title, body)
{
    $("#confirmTask").modal('hide');
    $('#alert-modal-title').html(title);
    $('#alert-modal-body').html(body);
    $('#alert-modal').modal('show');
}

$(document).ready(function()
{
    var boardId = $("#board_id").val();
    var orgId = $("#orgid").val();
    populateTasks(boardId);
    populateEmployees(orgId);
});

function addCommentForm(taskId)
{
    var formId = guid();

    var functionCall = 'submitComment(this,' + taskId + ')';
    var element = '<form class="form-horizontal" id="' + formId.trim() +
        '"><fieldset><legend>Form Name</legend>' +
        '<div class="form-group"> <label class="col-md-4 control-label" for="ctext">Comment Text</label> ' +
        '<div class="col-md-4"> <textarea class="form-control" id="ctext" name="ctext">Text</textarea> ' +
        '</div></div><div class="form-group"> <label class="col-md-4 control-label" for="submit-comment-form">' +
        '</label> <div class="col-md-4"> ' +
        '<button onclick="event.preventDefault();' + functionCall +
        '" id="submit-comment-form" ' +
        'name="submit-comment-form" class="btn btn-primary" data-id="' +
        formId + '">Submit</button></div></div></fieldset></form>';
    alertModal("New Comment", element);
}

function submitComment(id, task)
{
    console.log(id);
    var element = $("#" + $(id).data("id"));
    var comment = element.find("#ctext").val();
    var value = {
        "author_type": "manager",
        "text": comment,
        "task_id": task,
        "author_id": $("#manager-id").val()
    };
    console.log("yay" + id + " " + task)
    $.ajax(
        {
            type: "POST",
            url: $("#create-comment-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if (result.error != undefined)
                {
                    alertModal('Success', result.msg);
                }
                else
                {
                    $(".task").remove();
                    var boardId = $("#board_id").val();
                    populateTasks(boardId);
                    alertModal('Success', result.msg);
                }
            },
            error: function(result)
            {
                alertModal('Error', result.error);
            }
        });

}

function confirmEmpPin()
{
    var pin = $("#emp-pin-emp-display-pin").text();
    var action = $("#task-action").val();
    var task = $("#task-id").val();
    var value = {
        "pin": pin,
        "action": action,
        "task": task
    };
    $.ajax(
        {
            type: "POST",
            url: $("#mark-task-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if (result.error != undefined)
                {
                    alertModal('Success', result.msg);
                }
                else
                {
                    $(".task").remove();
                    var boardId = $("#board_id").val();
                    populateTasks(boardId);
                    alertModal('Success', result.msg);
                }
            },
            error: function(result)
            {
                alertModal('Error', result.error);
            }
        });
}

$("#emp-pin-confirm").click(function()
{

    confirmEmpPin();
});


function verifyPin()
{
    $("#emp-pin-emp-display").hide();
    $("#emp-pin-emp-display-name").hide();
    $("#emp-pin-emp-display-pin").hide();
    var value = {
        "pin": $("#emp-pin").val()
    };
    console.log('yay');
    $.ajax(
        {
            type: "POST",
            url: $("#get-employee-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if (result.employee != undefined)
                {
                    console.log(result.employee);
                    $("#emp-pin-form").fadeOut();
                    $("#emp-pin-emp-display-pin").css(
                        'background-color', result.employee.color
                    );
                    $("#emp-pin-emp-display-name").text(result.employee
                            .fname + " " + result.employee.lname);
                    $("#emp-pin-emp-display-pin").text(result.employee
                        .pin);
                    $("#emp-pin-emp-display").fadeIn();
                    $("#emp-pin-emp-display-name").fadeIn();
                    $("#emp-pin-emp-display-pin").fadeIn();
                }
                else
                {
                    $("#emp-pin-form-error").text(result.error);
                }
            }
        });
}

$("#verify-pin").click(function()
{
    verifyPin();
});

function sortTasks(employeeId)
{
    var todo = [];
    var done = [];
    $(".task").each(function()
    {
        var parent = $(this).parent().attr('id');
        var empId = $(this).find("#employee").data("id");
        if (parent == "todo" && empId == employeeId)
        {
            todo.push($(this));
            $(this).remove();
        }
        if (parent == "done" && empId == employeeId)
        {
            done.push($(this));
            $(this).remove();
        }
    });
    var i;
    for (i = 0; i < todo.length; i++)
    {
        $("#todo").prepend(todo[i]);
    }
    for (i = 0; i < done.length; i++)
    {
        $("#done").prepend(done[i]);
    }
}

function populateTasks(boardId)
{
    var value = {
        "board_id": boardId
    };
    $.ajax(
        {
            type: "POST",
            url: $("#get-tasks-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                var i;
                for (i = 0; i < result.tasks.length; ++i)
                {
                    var task = result.tasks[i];
                    var element = '<div id=\"task' + task.id +
                        '\" class=\"task animated fadeInDown' +// randomAnim() +
                        '\" data-id=\"' + task.id + '\"> ';
                    if (task.emp_abv  == "N/A")
                    {
                        element +=
                            '<div id="employee" class=\"taskEmp' +
                            // randomAnim() +
                            '\" style=\"background-color: ' +
                            '' + "lightGray" +
                            '\" > <h5 id="emp-name-d"></h5> </div>';
                    }
                    else
                    {
                        element +=
                            '<div ondblclick="sortTasks(' + task
                                .emp_id + ')" id="employee" class=\"taskEmp ' +
                            // randomAnim() +
                            '\" style=\"background-color: ' +
                            '' + task.color + '\" data-id="' + task
                                .emp_id + '"> <h5>' + task.emp_abv +
                            '</h5> </div>';
                    }
                    element += '<div class=\"taskContent ' +
                        // randomAnim() + 
                        '\"><h6>' + task.title +
                        '</h6>' +
                        '<div><p><span id=\"comment' + task.id +
                        '\">' + task.comments.length + ' ' +
                        '</span><span ondblclick="addCommentForm(' +
                        task.id +
                        ')" class=\"btnIcon glyphicon glyphicon-comment ' +
                        // randomAnim() + 
                        '\"></span>' +
                        '</p><span class=\"btn transparent btnIcon glyphicon glyphicon-chevron-down showComment\" ' +
                        'onclick="showComments(this)"></span> ' +
                        '</div></div>';
                    if(task.urgent == false)
                    {
                        element += '<div class=\"taskImportant\"></div><div id=\"commentsBlock0\">';
                    }
                    else
                    {
                        element += '<div style="background-color:#DB2929;" class=\"taskImportant\"></div>' +
                            '<div id=\"commentsBlock0\">';
                    }
                    if (task.comments.length > 0)
                    {
                        for (var j = 0; j < task.comments.length; j++)
                        {
                            var comment = task.comments[j];
                            if (comment != undefined)
                            {
                                element += '<p>* ' + comment.text +
                                    '</p> ';
                            }
                        }
                    }
                    element += '</div></div>';
                    if (task.unassigned == true)
                    {
                        $("#newTasks").append(element);
                        var count = parseInt($("#newTasksNumber").text());
                        $("#newTasksNumber").text(count + 1);
                    }
                    else if (task.todo == true)
                    {
                        $("#todo").append(element);
                        var count = parseInt($("#todoTasksNumber").text());
                        $("#todoTasksNumber").text(count + 1);
                    }
                    else
                    {
                        $("#done").append(element);
                        var count = parseInt($("#doneTasksNumber").text());
                        $("#doneTasksNumber").text(count + 1);
                    }
                    $("#newTasks, #todo, #done").sortable(
                        {
                            connectWith: ".dnd-container",
                            placeholder: "ui-sortable-placeholder",
                            start: function(event, ui) {},
                            stop: function(event, ui) {},
                            receive: function(event, ui)
                            {
                                ui.sender.sortable("cancel");
                                var source = ui.sender.attr(
                                    'id');
                                var destination = $(this).attr(
                                    'id');
                                var taskId = ui.item.attr(
                                    "data-id");
                                if (source ==
                                "done")
                                {
                                    alertModal("Error",
                                        "You can't mark a task already done as not done"
                                    )
                                }
                                else if ((destination == "todo" ||
                                    destination ==
                                    "done"))
                                {
                                    console.log(
                                        "Moving task id " +
                                        taskId +
                                        " from " +
                                        source + " to " +
                                        destination);
                                    $("#task-action").val(
                                        destination);
                                    $("#task-id").val(
                                        taskId);
                                    $("#confirmTask").modal(
                                        'show');
                                }
                                else if (destination ==
                                    "newTasks")
                                {
                                    alertModal("Error",
                                        "You can't move a task to the unassigned pile"
                                    )
                                }
                                else
                                {
                                    alertModal("Error",
                                        "Invalid Action"
                                    )
                                }
                            }
                        }).disableSelection();


                }
                fixHeight();
            }
        });
    cm()
}

function showComments(element)
{
    // save trigerrin button
    var element = $(element);

    var h = 0;
    if (element.hasClass('glyphicon-chevron-down'))
    {
        element.removeClass('glyphicon-chevron-down');
        element.addClass('glyphicon-chevron-up');
        element.parents('div.task').find('[id^="commentsBlock"]').slideToggle(
            'fast',
            function() {
                h = $(this).height();
            });
        //var ch = element.parents('div.task').find('[id^="commentsBlock"]').height();
        //$(".content").each(function () {
        //    $(this).height($(this).height() + ch);
        //});
    }
    else
    {
        element.removeClass('glyphicon-chevron-up');
        element.addClass('glyphicon-chevron-down');
        element.parents('div.task').find('[id^="commentsBlock"]').slideToggle(
            'fast',
            function() {
                h = $(this).height();
            });
    }
    var a = element.parents('div.task').find('[id^="commentsBlock:first"]');
    setTimeout(function(){
        $("div.content").height($("div.content").height() + h);
        fixHeight($("div.content").height());
    }, 100);
    
}

function populateComments(taskId)
{
    var value = {
        "task_id": taskId
    };
    $.ajax(
        {
            type: "POST",
            url: $("#get-comments-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                var i;
                for (i = 0; i < result.comments.length; ++i)
                {
                    var element = '<p id="comment' + i + '">' +
                        result.comments[i]['text'] +
                        '<span class="glyphicon glyphicon-remove remove ' +
                        // randomAnim() + 
                        '"></span></p>';
                    $("#comments-" + taskId).append(element);
                    $("#empsNumber").html(parseInt(this.val()) + 1);
                }
            }
        });
}

function sib(id)
{
    console.log(id);
    submitCreateTaskForm(id);
}

function enableEmployeeMode()
{
    $("#addTask").fadeOut();
     $("div#toggleMngMode").hide();
    $("#toggleEmpMode").fadeIn();
}

function disableEmployeeMode()
{
    $("#addTask").fadeIn();
    $("#toggleMngMode").fadeIn();
    $("#toggleEmpMode").hide();
}

function showLogin()
{
    $('#login-modal').modal('show');
}


function toggleEmployeeMode()
{
    var email = $("#te-email").val();
    var password = $("#te-password").val();
    var value = {
        "email": email,
        "password": password
    };
    $('#login-modal').modal('hide');
    $.ajax(
        {
            type: "POST",
            url: $("#login-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if (result.error != undefined)
                {
                    alertModal("Error", result.error);
                }
                else
                {
                    disableEmployeeMode();
                }
            }
        });
}

function submitCreateTaskForm(id)
{
    var element = $("#create-task-form-" + id);
    var taskName = element.find("#taskname").val();
    var taskDesc = element.find("#taskdesc").val();
    var emp = element.find("#employee").val();
    var man = element.find("#manager").val();
    var urgent = element.find("#urgent-1").val();
    var board = element.find("#selectboard").val();
    var hasErrors = false;
    if(isEmpty(taskName) || isEmpty(taskDesc))
    {
        hasErrors = true;
    }
    if(hasErrors)
    {
        alertModal("Error", "Invalid Task Details")
        return;
    }
    var data = {};
    data['board_id'] = board;
    data['task_title'] = taskName;
    data['task_desc'] = taskDesc;
    data['employee_id'] = emp;
    data['manager_id'] = man;
    data['urgent'] = false;
    if (urgent == "yes")
    {
        data['urgent'] = true
    }
    data = JSON.stringify(data);
    $.ajax(
        {
            url: $("#create-task-url").val(),
            type: 'POST',
            data: data,
            contentType: 'application/json;charset=UTF-8',
            cache: false,
            success: function(response)
            {
                if (response.error != undefined)
                {
                    alertModal("Error", response.error);
                }
                else
                {

                    alertModal("Success", "Created a new task. Reloading page..");
                    setTimeout(function ()
                    {
                        location.reload(true);
                    }, 2000);

                }
            },
            error: function(error)
            {
                alertModal("Error", error);
            }
        });
}

function createTaskForm()
{
    // create a new task
    var tid = guid();

    var newTask =
        '<form class="form-horizontal nosub" id="create-task-form-' + tid +
        '"><fieldset><legend>Create A Task</legend>' +
        '<div class=form-group><label class="col-md-4 control-label"for=selectbasic>Board</label><div class=col-md-6>' +
        '<select class=form-control id="selectboard" name=selectboard>';

    newTask += '<option value="' + $("#board_id").val() + '">' + $(
            "#board_name").val() + '</option>';

    newTask += '</select></div></div><div class=form-group>' +
        '<label class="col-md-4 control-label"for=taskname>Task Name</label><div class=col-md-6>' +
        '<input id=taskname name=taskname class="form-control input-md"placeholder="' +
        'Task name here like a title"required> ' +
        '<span class=help-block style="display: none; visibility: hidden;">help</span></div></div><div class=form-group>' +
        '<label class="col-md-4 control-label"for=taskdesc>Task Description</label>' +
        '<div class=col-md-6><input id=taskdesc name=taskdesc class="form-control input-md"placeholder="' +
        '...Task Description"> ' +
        '<span class=help-block style="display: none; visibility: hidden;">help</span></div></div><div class=form-group style="display: none; visibility: hidden;">' +
        '<label class="col-md-4 control-label"for=employee>Assign To Employee</label>' +
        '<div style="display: none; visibility: hidden;" class=col-md-6><select class=form-control id=employee name=employee>' +
        '<option value=none>None</option>';

    $(".employee").each(function()
    {
        newTask += '<option value="' + $(this).data("id") +
            '" style="' +
            'background-color: ' + $(this).css('backgroundColor') +
            '">' + $(this).children('#name').html() + '</option>'
    });

    newTask += '</select></div></div><div class=form-group style="display: none; visibility: hidden;">' +
        '<label class="col-md-4 control-label"for=employee>Manager</label><div class=col-md-6>' +
        '<select class=form-control id=manager name=manager>';

    newTask += '<option value="' + $("#manager-id").val() + '">' + $(
            "#manager-name").val() + '</option>';

    newTask +=
        '</select></div></div><div style="display: none; visibility: hidden;" class=form-group><label class="col-md-4 control-label"for=urgent>Mark As Urgent</label>' +
        '<div class=col-md-4><label class=radio-inline for=urgent-0><input id=urgent-0 name=urgent type=radio value=yes> Yes</label><label class=radio-inline for=urgent-1>' +
        '<input id=urgent-1 name=urgent type=radio value=no checked> No</label></div></div><div class=form-group><label class="col-md-4 control-label"for=taskname>' +
        '</label><div class=col-md-6>' +
        '<input type="button" class="btn btn-success" onclick="sib(\'' +
        tid + '\');" value="Create Task" />' +
        '</div></div></fieldset></form>';

    alertModal("New Task", newTask);
}

function populateEmployees(org)
{
    var value = {
        "org_id": org
    };
    $.ajax(
        {
            type: "POST",
            url: $("#get-employees-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                for (var i = 0; i < result.employees.length; ++i)
                {
                    var emp = result.employees[i];
                    var element = '<div id="employee-' + emp.id +
                        '" data-id="' + emp.id +
                        '" style=\"background-color:' + emp.color +
                        ' \" class="employee animated fadeInRight' +
                        //+ randomAnim() +
                        '" ondrag="dragg()"> <p id="name">' + emp.fname +
                        " " + emp.lname + '</p></div>';
                    $("#employees").append(element);
                    $("#empsNumber").html(parseInt($("#empsNumber")
                            .text()) + 1);
                }
            }
        });
}

function guid()
{
    function s4()
    {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}

/* Hacky as fuck do not try this at home*/
function fixHeight(hh)
{
    var eh = 0;
    if (typeof hh === 'undefined')
    {
        eh = 0;
    }
    else
    {
        eh = h;
    }
    var h = 0;
    $("div.content").each(function()
    {
        var number = $(this).height();
        if (number > h)
        {
            h = number + eh;
        }
    });
    $("div.content").height(h);
}

function cm()
{
    $.contextMenu({
        selector: ".task",
        callback: function(key, options) {
            var m = "clicked: " + key;
            window.console && console.log(m) || alert(m);
        },
        items: {
            foo: {name: "Assign To Employee", callback: function(key, opt)
            {
                var target = opt.$trigger;
                showAssignPanel(target.data("id"));
            }},
            bar: {name: "Toggle Urgency", callback: function(key, opt)
            {
                var target = opt.$trigger;
                toggleUrgency(target.data("id"));
            }},
            del: {name: "Delete Task", callback: function(key, opt)
            {
                var target = opt.$trigger;
                hideTask(target.data("id"));
            }}
        }
    });
}

function showAssignPanel(id)
{

    var value = {
        "org_id": $("#orgid").val()
    };
    var did = guid();
    $.ajax(
        {
            type: "POST",
            url: $("#get-employees-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                var data = '';
                for (var i = 0; i < result.employees.length; ++i)
                {
                    var emp = result.employees[i];
                    data[emp.pin] = emp.fname + emp.lname;
                    data += '<option style="background-color:' + emp.color + '" value="'+ emp.pin +'">' + emp.fname + " " + emp.lname + '</option>';
                }
                var element = '<form class="form-horizontal" id="'+ did +'"><fieldset><legend>Form Name</legend><div class="form-group"> ' +
                    '<label class="col-md-4 control-label" for="employee">Employee</label> ' +
                    '<div class="col-md-4"> <select id="employee" name="employee" class="form-control"> ' +
                    '' + data +'</select>' +
                    ' </div></div><div class="form-group"> <label class="col-md-4 control-label" for="singlebutton">' +
                    '</label> <div class="col-md-4"> <input type="hidden" id="tid" value="' + id + '"> ' +
                    '<button id="singlebutton" name="singlebutton" data-id="'+ did +'"class="btn btn-primary" onclick="event.preventDefault();' +
                    'assignTask(this);">Assign Task</button> ' +
                    '</div></div></fieldset></form>';

                alertModal("Assign To Employee", element);
            }
        });
    //assign_task-url
}

function assignTask(form)
{
    var taskId = $(form).data("id");
    form = $("#" + taskId);
    var value = {
        "emp": form.find("#employee").val(),
        "task": form.find("#tid").val()
    };
    console.log(value);
    $.ajax(
        {
            type: "POST",
            url: $("#assign_task-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if(result.error != undefined)
                {
                    alertModal("Error", result.error)
                }
                else
                {
                    alertModal("Assign To Employee", result.msg);
                    $(".task").remove();
                    var boardId = $("#board_id").val();
                    populateTasks(boardId);
                }
            }
        });
}

function hideTask(id)
{
    //
    var value = {
        "task": id
    };
    $.ajax(
        {
            type: "POST",
            url: $("#hide_task-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if(result.error != undefined)
                {
                    alertModal("Error", result.error());
                }
                alertModal("Success", result.msg);
                $(".task").remove();
                var boardId = $("#board_id").val();
                populateTasks(boardId);

            }
        });
}
function toggleUrgency(id)
{
    //toggle_urgency-url
    var value = {
        "task": id
    };
    $.ajax(
        {
            type: "POST",
            url: $("#toggle_urgency-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if(result.error != undefined)
                {
                    alertModal("Error", result.error());
                }
                alertModal("Success", result.msg);
                $(".task").remove();
                var boardId = $("#board_id").val();
                populateTasks(boardId);

            }
        });
}

function isEmpty(str)
{
    if(str.replace(/\s/g,"") == "")
    {
        return true;
    }
    return false;
}


