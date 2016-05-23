/**
 * Customising jquery functions
 */
var boardCount = 0;
var employeeCount = 0;

var empColors = [
    "#CFAFAF",
    "#E7A1A1",
    "#DDDDA8",
    "#E9D2D2",
    "#FFECE5",
    "#CDB2A5",
    "#FFCD72",
    "#D86F36",
    "#FEECA1",
    "#E2E095",
    "#D9D9BF",
    "#CCE281",
    "#B5D397",
    "#B7E2B7",
    "#CCE281",
    "#96E5CD",
    "#8DE0CD",
    "#8BD5C7",
    "#9CEDE9",
    "#E4B29A",
    "#99bbff",
    "#C1D2D2",
    "#A4C9C9",
    "#D2C9C1",
    "#FFB872",
    "#AFE2EB",
    "#B8DBE6",
    "#C2D4DE",
    "#C7E8FD",
    "#C4D5E7",
    "#E8EAFA",
    "#B2ABDA",
    "#BEB2D7",
    "#F2BA49",
    "#FFB347",
    "#C7C0CD",
    "#D0A9F3",
    "#E1D4E8",
    "#E7DCE7",
    "#F69DAF",
    "#CFAAC7"
];

$(function()
{

    var orgId = parseInt($("#orgid").val());
    populateBoards(orgId);
    populateEmployees(orgId);

    makeEmpsDraggable();

    // add a new board
    $("#addBoard").click(function()
    {
        var newId = guid();
        var newBoard =
            '<div class="col-sm-3" id="' + newId +
            '"><div class="board board-new"><div><h4 class="heading">New Board</h4>' +
            '<button class="btn transparent delete remove">X</button></div><br/>' +
            '<form><fieldset class="form-group"><input type="text" class="form-control input"' +
            ' id="boardTitle" placeholder="Board Title"> </fieldset><fieldset class="form-group">' +
            '<textarea class="form-control input" id="boardDesc" placeholder="Description" rows="2"></textarea>' +
            '</fieldset></div><div class="text-center">' +
            '<button class="btn brd" id="create-board" data-id="' + newId +
            '" onclick="createBoard(this)">Save</button></form></div></div>';
        $("#boards").parent().prepend(newBoard);
        boardCount++;
        //$("#boardsNumber").text(boardCount);
        document.getElementById("create-board").addEventListener(
            "click",
            function(event)
            {
                event.preventDefault()
            });

        // make employees droppable at the board
        makeEmpsDraggable();
    });

    // add new employee
    $("#addEmployee").click(function()
    {
        createEmployeeForm();

        // make employee draggable to board
        makeEmpsDraggable();
    });

})

// remove board or employee
    .on('click', '.remove', function()
    {

        // checks if event source is from board or employee
        if ($(this).parent().parent().attr('class') == 'board board-new')
        {
            $(this).parentsUntil("#boards").remove();
            boardCount--;
            $("#boardsNumber").text(boardCount);
        }
        else
        {
            $(this).parentsUntil("#employees").remove();
            employeeCount--;
            $("#empsNumber").text(employeeCount);
        }
    })


    // save board or employee
    .on('click', '.save', function()
    {

        $(this).remove();
    })

    // edit board
    .on('click', '.menu', function()
    {

        var rootBoard = $(this).parents('div.col-sm-3');
        var boardId = $(rootBoard).attr('id').substr(-1);

        var editBoard =
            '<div class="board board-new"><div><h4 class="heading">Edit Board</h4>' +
            '<button class="btn transparent delete cancel">X</button></div><br/>' +
            '<form><fieldset class="form-group"><input type="text" class="form-control input"' +
            ' id="boardTitle' + boardId +
            '" placeholder="Board Title" value="' +
            $(rootBoard).find('h2.text-center').text() +
            '"></fieldset><fieldset class="form-group">' +
            '<textarea class="form-control input" id="boardDesc' + boardId +
            '" placeholder="Description" rows="2">' +
            $(rootBoard).find('p.description').text() + '</textarea>' +
            '</fieldset><p>Employees:  </p><div id="empsInvolved' + boardId +
            '" class="emps"></div><div class="text-center"><button class="btn brd remove">Delete</button> ' +
            '<button class="btn brd save">Save</button></form></div></div>';

        $(rootBoard).children().hide();
        $(rootBoard).append(editBoard);
    })

    // edit employee
    .on('dblclick', '.employee', function()
    {
        // alert("The paragraph was double-clicked");s

        var rootEmployee = $(this).closest('div.employee');
        // check that employee div is not the new dive or edit div
        if (!$(rootEmployee).hasClass('employee-new'))
        {
            var employeeId = $(rootEmployee).attr('id').substr(-1);

            var editEmployee =
                '<div class="heading"><p>Edit Employee</p><button class="btn transparent delete cancel">X</button>' +
                '</div><form><fieldset class="form-group"><input type="text" class="form-control input" id="firstName' +
                employeeId + '" placeholder="First Name" value="' + $(
                    rootEmployee).find('span:first-child').text() +
                '" autocomplete="off"><input type="text" class="form-control input" id="lastName' +
                employeeId + '" placeholder="Last Name" value="' + $(
                    rootEmployee).find('span:last-child').text() +
                '" autocomplete="off"><input type="text" class="form-control input" id="phone' +
                employeeId +
                '" placeholder="Phone Number" autocomplete="off"></fieldset>' +
                '<div class="text-center"><p>PIN</p><span>: AP1023</span></div><div class="text-center">' +
                '<button class="btn brd remove">Delete</button><button class="btn brd save">Save</button></div></form></div>';

            $(rootEmployee).children().hide();
            $(rootEmployee).append(editEmployee).addClass('employee-new');
        }
    })


    // cancel editting boards or employees
    .on('click', '.cancel', function()
    {

        if ($(this).parent().parent().attr('class') == 'board board-new')
        {
            var rootBoard = $(this).parents('div.col-sm-3');
            $(rootBoard).find('div:first-child').show();
            $(rootBoard).find('div.board-new').remove();
        }
        else
        {
            var rootEmployee = $(this).closest('div.employee');
            $(rootEmployee).removeClass('employee-new').find('p').show();
            $(rootEmployee).find('div').remove();
            $(rootEmployee).find('form').remove();
        }
    })
    // focus on text field
    .on('click', '.input', function()
    {
        $(this).focus();
    }
);

/**
 * Function to redirect to board page when board double clicked
 */
function goToBoard(id)
{
    window.location.href = $("#base-url").val() + "showboard/" + id;
}

/**
 * Function to make employees draggable to boards
 */
function makeEmpsDraggable()
{
    $('#employees, [id^="empsInvolved"]').sortable(
        {
            connectWith: ".emps"
        }).disableSelection();
}

function createEmployee(form)
{
    form = $("#" + $(form).data("id"));
    var fn = form.find("#first-name").val();
    var ln = form.find("#last-name").val();
    var c = form.find("#color").val();
    var value = {
        "first-name": fn,
        "last-name": ln,
        "color": c,
        "org": $("#orgid").val()
    };
    console.log(value);
    $.ajax(
        {
            type: "POST",
            url: $("#create-employee-url").val(),
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
                    var element = '<div id="emp-pin-emp-display"> <h1 id="emp-pin-emp-display-name"></h1> ' +
                        '<h1>A new employee has been created!</h1><h1 id="emp-pin-emp-display-pin"></h1> </div>';
                    alertModal("Success", element);
                    $("#emp-pin-emp-display-pin").css({
                        'background-color': result.employee.color,
                        'padding': '5px 0px',
                        'border-radius': '3px',
                        'text-align': 'center'
                    });
                    
                    $("#emp-pin-emp-display-name").text(result.employee
                            .fname + " " + result.employee.lname);
                    $("#emp-pin-emp-display-pin").text(result.employee
                        .pin);
                    $("#emp-pin-emp-display").fadeIn();
                    $("#emp-pin-emp-display-name").fadeIn();
                    $("#emp-pin-emp-display-pin").fadeIn();
                    $(".employee").remove();
                    var orgId = parseInt($("#orgid").val());
                    populateEmployees(orgId);
                }
            }
        });
}

function populateBoards(orgId)
{
    var value = {
        "org_id": orgId
    };
    $.ajax(
        {
            type: "POST",
            url: $("#get-boards-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                if (result.boards == undefined)
                {
                    alertModal("Error",
                        "An Error occurred while loading the boards"
                    )
                }
                else if (!result.boards.length > 0)
                {
                    alertModal("Error",
                        "This company does not have any boards"
                    )
                }
                else
                {
                    for (var i = 0; i < result.boards.length; ++i)
                    {
                        var b = result.boards[i];
                        //noinspection JSUnresolvedVariable
                        addBoard(b.id, b.name, 0, b.desc, String(b.count));

                    }
                }
            }
        });
}

$("#create-board").click(function()
{
    alert("Handler for .click() called.");
});

function createEmployeeForm()
{
    var formId = guid();
    var form = '<form class="form-horizontal" id="'+ formId +'"><fieldset><legend>Create an Employee</legend><div class="form-group"> ' +
        '<label class="col-md-4 control-label" for="first-name">First Name</label> <div class="col-md-4"> ' +
        '<input id="first-name" name="first-name" type="text" placeholder="First Name" class="form-control input-md" required=""> ' +
        '</div></div><div class="form-group"> <label class="col-md-4 control-label" for="last-name">Last Name</label> ' +
        '<div class="col-md-4"> <input id="last-name" name="last-name" type="text" placeholder="Last Name" class="form-control input-md" required=""> ' +
        '</div></div><div class="form-group"> <label class="col-md-4 control-label" for="textinput">Employee Color</label> ' +
        '<div class="col-md-4">' +
        ' <div id="cp11" class="input-group">' +
        '<select id="color" name="color" class="form-control" style="background-color:' + empColors[0] +'!important"> ';
    for (var i = 0; i < empColors.length; ++i)
    {
        form += '<option style="background-color:' + empColors[i] +'!important" value="' + empColors[i] +'">' + empColors[i] +'</option> ';
    }
    form +='</select></div></div></div><div class="form-group"> ' +
        '<label class="col-md-4 control-label" for="singlebutton"></label> <div class="col-md-4"> ' +
        '<button id="singlebutton" data-id="'+ formId +'" name="singlebutton"  onclick="event.preventDefault();' +
        'createEmployee(this);" class="btn btn-primary">Create Employee</button> </div></div></fieldset></form>';

    alertModal("", form);
    $('#color').on('change', function(){
        var selected = $(this).find("option:selected").val();
        $(this).css("background-color", selected);
    });
}

function createBoard(element)
{
    var id = $(element).data("id");
    element = $("#" + id);
    var title = element.find('#boardTitle').val();
    var desc = element.find('#boardDesc').val();
    var managerId = $("#manager-id").val();
    var orgId = $("#orgid").val();
    var value = {
        "manager": managerId,
        "title": title,
        "desc": desc,
        "org_id": orgId
    };
    element.remove();
    $.ajax(
        {
            type: "POST",
            url: $("#create-board-url").val(),
            data: JSON.stringify(value),
            contentType: 'application/json;charset=UTF-8',
            success: function(result)
            {
                console.log(result);
                if (result.error != undefined)
                {
                    alertModal("Error", result.error);
                }
                else
                {
                    var b = result.board;
                    alertModal("Success", result.msg);
                    addBoard(b.id, b.name, 0, b.desc, b.count);
                }
            }
        });
}

function addBoard(id, title, numberOfEmps, desc, count)
{
    var board =
        '<div class="board col-md-6" data-id="' + id + '"ondblclick="goToBoard(' +
        id + ')"><div class="board-inner"><div><h2 class="text-center" id="title">' + title + '</h2>' +
        '<button data-id="' + id + '" class="btn transparent menu btnIcon glyphicon glyphicon-align-justify" onclick="event.preventDefault();' +
        'showEditBoardForm(this);"></button>' +
        '</div><br/><div class="text-center"><h2>' + count +
        ' <span class="glyphicon glyphicon-tasks"></span></h2>' +
        '</div><hr/><div><p class="description" id="desc">' + desc + '</p>' +
        '</div></div></div>';

    $("#boards").append(board);
    $("#boardsNumber").html(parseInt($("#boardsNumber").text()) + 1);
}

function alertModal(title, body)
{
    $('#alert-modal-title').html(title);
    $('#alert-modal-body').html(body);
    $('#alert-modal').modal('show');
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
                    var element =
                        '<div id="employee_2" style=\"background-color:' +
                        emp.color +
                        ' \" class="employee" ondrag="dragg()"> <p>' +
                        emp.fname + " " + emp.lname + '</p></div>';
                    $("#employees").append(element);
                    $("#empsNumber").html(parseInt($("#empsNumber")
                            .text()) + 1);
                }
            }
        });
}

function showEditBoardForm(source)
{
    var id = guid();
    var bid = $(source).data("id");
    var title =  "placeholder";
    var desc =  "placeholder";
    $(".board").each(function () {
       if($(this).data("id") == bid)
       {
           title = $(this).find("#title").text();
           desc = $(this).find("#desc").text();
           return false;
       }
    });

    var element = '<form class="form-horizontal" id="'+ id +'"><fieldset><legend>Form Name</legend>' +
        '<div class="form-group"> <label class="col-md-4 control-label" for="title">Title</label>' +
        '<div class="col-md-4"> <input id="title" name="title" type="text" ' +
        'placeholder="Title Goes Here" class="form-control input-md" required="" value="'+ title +'"> ' +
        '</div></div><div class="form-group"> <label class="col-md-4 control-label" for="desc">' +
        'Description</label> <div class="col-md-4"> <input id="desc" name="desc" type="text" ' +
        'placeholder="Description goes here" class="form-control input-md" value="'+ desc +'"> </div></div>' +
        '<div class="form-group"> <label class="col-md-4 control-label" for="singlebutton">' +
        '</label> <div class="col-md-4"> <button id="singlebutton" ' +
        'name="singlebutton" class="btn btn-primary" onclick="event.preventDefault();' +
        'editBoard(this);" data-id="'+ id +'" data-board="'+ bid +'">Submit Changes</button> </div></div>' +
        '</fieldset></form>';
    alertModal("Edit A Board", element);
}

function editBoard(id) {
    var form = $("#" + $(id).data("id"));
    var title = form.find("#title").val();
    var desc = form.find("#desc").val();
    var idd = $(id).data("board");
    var value = {
        "id": idd,
        "title": title,
        "desc": desc
    };
    $.ajax(
        {
            type: "POST",
            url: $("#edit-board-url").val(),
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
                    alertModal("Success", result.msg + " .Reloading page..." );
                    setTimeout(function () {
                        location.reload(true);
                    }, 3000);
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