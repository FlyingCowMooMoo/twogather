/**
 * Customising jquery functions
 */
var boardCount = 0;
var employeeCount = 0;
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
            '</fieldset><p>Employees:  </p><div id="empsInvolved' +
            boardCount +
            '" class="emps"></div><div class="text-center">' +
            '<button class="btn brd" id="create-board" data-id="' +
            newId +
            '" onclick="createBoard(this)">Save</button></form></div></div>';
        $("#boards").append(newBoard);
        boardCount++;
        $("#boardsNumber").text(boardCount);
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

        // generate random PIN number
        var randomPIN = Math.floor(Math.random() * (99999 -
            10000 + 1) + 10000);
        var newEmployee =
            '<div id="employee' + employeeCount +
            '" class="employee employee-new">' +
            '<div class="heading"><p>New Employee</p><button class="btn transparent delete remove">X</button>' +
            '</div><form><fieldset class="form-group"><input type="text" class="form-control input" id="firstName' +
            employeeCount + '"' +
            ' placeholder="First Name" autocomplete="off"><input type="text" class="form-control input" id="lastName' +
            employeeCount +
            '" placeholder="Last Name" autocomplete="off">' +
            '<input type="text" class="form-control input" id="phone' +
            employeeCount +
            '" placeholder="Phone Number" autocomplete="off"></fieldset>' +
            '<div class="text-center"><p>PIN</p><span>: E' +
            randomPIN +
            '</span></div><div class="text-center">' +
            '<button class="btn brd save">Save</button></div></form></div>';
        $("#employees").append(newEmployee);
        employeeCount++;
        $("#empsNumber").text(employeeCount);

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

        // checks if event source is from board or employee
        console.log($(this));
        if ($(this).parent().parent().parent().attr('class') ==
            'board board-new')
        {

        }
        else
        {
            var employee =
                '<p><span>' + $(this).parents('form').find(
                    '[id^="firstName"]').val() + '</span> <span>' +
                $(this).parents('form').find('[id^="lastName"]').val() +
                '</p>';
            var rootEmployee = $(this).parents('div.employee');
            $(rootEmployee).empty();
            $(rootEmployee).append(employee).removeClass('employee-new');
        }
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
    });

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
    console.log(value);
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
                    addBoard(b.id, b.name, 0, b.desc, b.count);
                }
            }
        });
}

function addBoard(id, title, numberOfEmps, desc, count)
{
    var board =
        '<div class="board" data-id="' + id + '"ondblclick="goToBoard(' +
        id + ')"><div><h2 class="text-center">' + title + '</h2>' +
        '<button class="btn transparent menu glyphicon glyphicon-align-justify"></button>' +
        '</div><br/><div class="text-center"><h2>' + numberOfEmps +
        ' <span class="glyphicon glyphicon-user"></span></h2><h2>' + count +
        ' <span class="glyphicon glyphicon-tasks"></span></h2>' +
        '</div><hr/><div><p class="description">' + desc + '</p>' +
        '</div></div>';

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