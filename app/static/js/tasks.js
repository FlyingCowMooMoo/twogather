/**
 * This javaScript file handls the functions including jQuery for the tasks page
 */
var taskCount = 0;
 $(function() {

 	// make employees draggable
 	makeEmpsDraggable()

 	$("#addTask").click( function(){

 		// create a new task
 		var newTask =
 			'<div id="task' + taskCount + '" class="task task-new parent"><div class="heading">' +
          	'<h5>New Task</h5><span class="glyphicon glyphicon-remove remove"></span></div><form>' +
            '<fieldset class="form-group"><input type="text" class="form-control input" id="taskTitle' +
            taskCount + '" placeholder="Task Title"></fieldset><p>Employee:</p><div id="empAssigned' +
            taskCount + '" class="input emps"></div><div id="comments' + taskCount + '"></div><fieldset ' +
            'class="form-group"><input type="text" class="form-control input" id="comment' + taskCount + 
            '0" placeholder="Comment"><button type="button" class="btn brd addComment">Add Comment</button></fieldset><div>' +
            '<h5>Set as important:  </h5><input id="taskImportant' + taskCount + '" type="checkbox">' +
            '</input></div><div class="text-center"><button type="button" class="btn brd save">Save</button></div></form></div>';

 		$("#newTasks").append(newTask);
 		taskCount ++;
 		$("#todoTasksNumber").text(taskCount);
 	});

 })

// remove board or employee
.on('click', '.remove', function() {

	var rootElement = $(this).closest('.parent');

	// checks whether it is a task or a comment to be deleted
	if ($(rootElement).hasClass('task')) {

		// checks for the closest element with the class parent, then deletes it
		$(rootElement).remove();
		taskCount --;
		$("#todoTasksNumber").text(taskCount);
	}
	else {
		$(rootElement).remove();
	}

})

// add a commen to the task
.on('click', '.addComment', function() {

	// find task id and number of comments if there any
	var task = $(this).parents('div.task');
	var commentsDiv =  $(task).find('[id^="comments"]');
	// var taskId = $(this).parent('div.task').attr('id').substr(-1);
	var commentCount = $(commentsDiv).children().length;
	// var commentCount = 0;
	var newComment = 
		'<p id="comment' + commentCount +'" class="parent"><span>* ' + $(this).prev().val() + 
		'</span><span class="glyphicon glyphicon-remove remove"></span></p>';
	$(commentsDiv).append(newComment);
})

.on('click', '.save', function(){

	var rootTask = $(this).parents('div.task');
	var taskId = $(rootTask).attr('id').substr(-1);
	var taskEmp = $(rootTask).find('[id^="employee_"]');
	var taskEmpId = $(taskEmp).attr('id');//.substr(-1);
	var taskComments = $(rootTask).find('[id^="comments"]');
	var task = '';

	// check if employee is already assigned
	if (taskEmpId == null){
		task += '<div class="taskEmp" style="background-color:lightGray;"></div>'
	}
	else {
		task += '<div id="' + taskEmpId + '" class="taskEmp"><h3>' + $(taskEmp).find('p').text().substr(0,2) +
        	'</h3></div>'
	}

	task +=
		'<div class="taskContent"><h6>' + $(rootTask).find('[id^="taskTitle"]').val() + '</h6><div>' +
        '<p><span id="comment' + taskId + '"> ' + $(rootTask).find('[id^="comments"]').children().length + 
        ' </span><span class="glyphicon glyphicon-comment"></span></p><span class="btn transparent glyphicon' +
        ' glyphicon-chevron-down showComment"></span></div></div>';

    // check if task was set as important
    if ($(rootTask).find('[id^="taskImportant"]').is(':checked')){
    	 task += '<div class="taskImportant" style="background-color:#db4141;"></div>';
    }else {
    	task += '<div class="taskImportant"></div>';
    }

    task += '<div id="commentsBlock' + taskId + '">'; 


    // add all comments task
    $(taskComments).children().each( function(){
    	task += '<p>' + $(this).children().first().text() +  '</p>';
    });

    task += '</div>';

    addLog("You added task '" + $(rootTask).find('[id^="taskTitle"]').val() + "'.");

    // empty task block and fill it with the detaiils
    $(rootTask).empty().attr('class','task').append(task);


})

// show the comments block
.on('click', '.showComment', function(){

	// save trigerrin button
	var button = $(this);

	// show comments block then change button icon
	$(this).parents('div.task').find('[id^="commentsBlock"]').slideToggle('fast', function() {

		if($(button).hasClass('glyphicon-chevron-down')){
			$(button).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
		}
		else {
			$(button).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
		}
	});


})

// edit employee
.on('dblclick', '.taskEmp', function(){
    // alert("The paragraph was double-clicked");s

    var rootTask =  $(this).parent();

    var taskId = $(rootTask).attr('id').substr(-1);

    var empId = "";
    if ($(this).find('div.taskEmp').attr('id)') != null){
    	empId = $(this).find('div.taskEmp').attr('id)');
    }

    var comments = $(rootTask).find('[id^="commentsBlock"]');
    var commentCount = 0;
    var editTask = 
      	'<div class="heading"><h5>Edit Task</h5><span class="glyphicon glyphicon-remove cancel"></span>' +
      	'</div><form><fieldset class="form-group"><input type="text" class="form-control input"' + 
      	' id="taskTitle' + taskId + '" placeholder="Task Title" value="' + $(rootTask).find('h6').text() + '">'+
        '</fieldset><p>Employee:</p><div id="' + empId + '" class="input"></div><div id="comments' + taskId + 
        '">';

    $(comments).children().each( function(){
    	editTask += '<p id="comment' + commentCount + '">' + $(this).text() +
    		'<span class="glyphicon glyphicon-remove remove"></span></p>';
    });    

    editTask +=
        '</div><fieldset class="form-group"><input type="text" class="form-control input" placeholder="Comment">' +
        '<button type="button" class="btn brd">Add Comment</button></fieldset><div><h5>Set as important:  </h5>' +
        '<input id="taskImportant0" type="checkbox"></input></div> <div class="text-center"><button type="button"' +
        ' class="btn brd remove">Delete</button><button type="button" class="btn brd save">Save</button></div></form>';	

    $(rootTask).children().hide();
    $(rootTask).append(editTask).addClass('task-new').addClass('parent');	
});

function addTask(taskId, taskName, empName)
{

	populateComments(taskId);
}

function populateComments(taskId)
{
	var value = {"task_id": taskId};
	$.ajax({
		type : "POST",
		url : "{{ url_for('get_comments') }}",
		data: JSON.stringify(value),
		contentType: 'application/json;charset=UTF-8',
		success: function(result) {
			var i;
			for (i = 0; i < result.comments.length; ++i) {
				var element = '<p id="comment' + i + '">' + result.comments[i].text +
					'<span class="glyphicon glyphicon-remove remove"></span></p>';
				//var element = " <blockquote class=\"\" data-id=" + i + "\"><p><cite>" + result.comments[i].text + "</cite> </p> <small>" + result.comments[i].author + "</small>";
				$("#comments-" + taskId).append(element);
			}
			console.log(result);
		}
	});
}


function populateEmployees(org) {
	var value = {"org_id": org};
	$.ajax({
		type: "POST",
		url: "{{ url_for('get_employees') }}",
		data: JSON.stringify(value),
		contentType: 'application/json;charset=UTF-8',
		success: function (result) {
			for (var i = 0; i < result.employees.length; ++i) {
				var emp = result.employees[i];
				var ele = '<div id="employee_2" style=\"background-color:" + emp.color + " \" class="employee" ondrag="dragg()"> <p>'+ emp.fname + " " + emp.lname +'</p></div>';
				var emp = result.employees[i];
				var element = " <blockquote  style=\"background-color:" + emp.color + " \" class=\"\" data-id=" + emp.id + "\"><p><cite>" + emp.fname + " " + emp.lname + "</cite> </p> <small>" + emp.pin + "</small>";
				$("#employees").append(element);
			}
		}
	});
}

/* Activity logs */
var logs = [];

function addLog(log) {
    
    logs.push(log);
}



