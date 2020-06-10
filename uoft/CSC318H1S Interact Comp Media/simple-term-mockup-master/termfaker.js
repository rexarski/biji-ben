var kc_enter = 13;

var CONTEXT_SHELL = "CONTEXT_SHELL"
var context = CONTEXT_SHELL

var input_area = $("#input-area");
var msg_buffer = $("#message-buffer");

$.ready(function() {
 	input_area.focus();
	// Force focus
	input_area.focusout(function(){
		input_area.focus();
	});
});

input_area.keydown(function(evt){
	//console.log(evt.keyCode);
	if (evt.keyCode == kc_enter) {
		evt.preventDefault();
		sendCommand();
	}
})


function sendMsg(sender, content, rc) {
	msg_buffer.append($(
			"<section class='message' data-sender='"+sender+"' data-rc="+rc+">" +
			content +
			"</section>"
			));
	msg_buffer.animate({scrollTop: msg_buffer[0].scrollHeight-msg_buffer.height()}, 200);
}

function sendCommand() {
	var val = input_area.val();
	if (val != "") {
		sendMsg("me@localhost", val);
	}
	setTimeout(
		function(){parseInput(val)},
		200);
	input_area.val("");
}
parseInput = callCommand

commandMap = {
	ls: _ls,
	where: _ls,
	location: _ls,
	dir: _ls,
	l: _ls,
	clear: _clear,
	cd: _cd,
	enter: _cd,
	go: _cd,
	go_to: _cd,
	rm: yn_rm,
	remove: yn_rm,
	'delete': yn_rm
}

function callCommand(cmd) {
	if (cmd != ""){
		_cmd = cmd.toLowerCase()
		if (_cmd.indexOf("how do i ") == 0 || _cmd.indexOf("? ") == 0) {
			disp_response({
				rc: 0,
				msg: $("#help_query").html(),
				sender: "helpbot"});

		} else {
			console.log("calling '"+cmd+"'");
			var argv = cmd.split(" ");
			var response = {
				rc: 1,
				msg: "Unknown command '"+argv[0] +
						"'. Try asking for help?",
				sender: "shellbot"};

			if (argv[0].toLowerCase() == "help") {
				response = _help(argv);
				if (response != null) {	
					response.sender = "helpbot";			
				}
			} else if (argv[0].toLowerCase() in commandMap) {
				response = commandMap[argv[0].toLowerCase()](argv)
				if (response != null) {
					response.sender = "shellbot";
				}
			}
			// response is an object of form
			// { rc = (0|1),
			//   msg = "..." }

			//send the actual message
			disp_response(response)	
		}
	}
}

function disp_response(response) {
	if (response != null) {
		$(msg_buffer.children()[msg_buffer.children().length-1]).attr('data-rc', response.rc)
		sendMsg(response.sender, response.msg, response.rc)		
	}		
}

function display_blocktext(sender, strings) {
	sendMsg(sender, strings.splice(0,1));
	if (strings.length > 0) {
		parseInput = function() {
			display_blocktext(sender, strings)
		}
	}
	else {
		parseInput = callCommand;
	}
}

function get_yn(sender, prompt, callback) {
	sendMsg(sender, prompt + " (yes/no)", 0)
	parseInput = function (msg) {
		var val = null;
		switch (msg) {
			case "yes":
				val = true
				break;
			case "y":
				val = true
				break;
			case "n":
				val = false
				break;
			case "no":
				val = false
				break;
			default:
				get_yn(sender,prompt,callback)
		}
		if (val != null) {
			parseInput = callCommand;
			callback(val);			
		}
	}
}

function _help (argv) {
	if (argv.length == 1) {
		return {
			rc: 0,
			msg: $("#helpTemplate").html()
		};
	}

	switch (argv[1]) {
		case "interface":
			display_blocktext("helpbot", 
				$.map($(".helptext_body.interface"),
					function(e){
						return $(e).html();
					}));
			return null;
		default:
			return {
				rc: 1,
				msg: "I was kidding, help is not implemented :("
			};
	}

}

function _ls (argv) {
	var rows = 5
	var content = $("#sidebar ul li");
	splits = Math.ceil(content.length/rows);
	var buildHTML = "";
	for (var s=0; s<splits; s++){
		buildHTML = buildHTML + "<ul class='lsout'>"
		for (var i=s*rows; i< Math.min((s+1)*rows, content.length); i++) {
			buildHTML = buildHTML + content[i].outerHTML;
		}
		buildHTML = buildHTML + "</ul>"
	}

	return {
		rc: 0,
		msg: buildHTML
	};
}


function _clear (argv) {
	msg_buffer.html("");
	return null;
}

function yn_rm(argv) {
	var msg = ""
	for (var i=1; i<argv.length; i++) {
		if (i != 1 && i == argv.length - 1){
			msg = msg + ", and '"+ argv[i]+"'";
		} else if (i!= 1) {
			msg = msg + ", '"+ argv[i] + "'";
		} else {
			msg = msg +" '"+argv[i]+"'"
		}
	}
	get_yn(	"shellbot",
			"delete"+msg+"?",
			function(yn) {
				if (yn) {
					resp = _rm(argv);
					if (resp != null) {
						resp.sender = "shellbot"
					}
					disp_response(resp);
				}
			});
}

function _rm(argv) {
	argv.splice(0,1)
	failures = []
	for (i in argv) {
		if (deletefile(argv[i])) {
			failures.push(argv[i]);
		}
	}
	update_cwd_tree(".");
	if(failures.length > 0) {
		return {
			rc: 1,
			msg: "files ("+failures.join(", ")+") could not be found"
		}
	}
}

function _cd (argv) {
	if(!update_cwd_tree(argv[1])) {
		return {
			rc: 1,
			msg: "no such file or directory "+argv[1]
		}
	}
	return null;
}
