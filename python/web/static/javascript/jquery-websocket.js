new function() {
	var ws = null;
	var connected = false;

	var serverUrl;
	var connectionStatus;
	var sendMessage;
	var currentSender="me";
	var currentUser;
	var idMessage=0;

	var open = function(url ,user) {
	
		ws = new WebSocket(url);
		ws.onopen = onOpen;
		ws.onclose = onClose;
		ws.onmessage = onMessage;
		ws.onerror = onError;
		currentUser=user;


	}
	
	var close = function() {
		if (ws) {
			console.log('CLOSING ...');
			ws.send(buildJsonMessage(currentUser,"disconnecting","DISCONNECT"));
			ws.close();
		}
		
	}
	
	
	var onOpen = function() {
		console.log('OPENED: ' + serverUrl);
		connected = true;
		$("#theBubbles").append("<div id=lastbubble_"+ idMessage + " class=\"bubble me message\">Connected to PimpMyGPS socket !</div>");
		ws.send(buildJsonMessage(currentUser,"connecting","POSTMESSAGE"));
	};
	
	var onClose = function() {
		console.log('CLOSED: ' + serverUrl);
		
		
		ws = null;
	};
	
	function sendToBubble(jsonMessage)
	{
		$( "#lastbubble_" + (idMessage - 1) ).each(function( index ) {
			$(this).addClass("animated fadeOutUp");
		});
		
		idMessage++;
		if ( currentSender == "you")
			{
			currentSender="me";
			}else
				{
				currentSender="you";
				}
			$("#theBubbles").append("<div id=lastbubble_"+ idMessage + " class=\"bubble " + currentSender +" message\"><img style=position:relative;top:-4px;left:-16px height=24px width=24px src=avatars/" + jsonMessage.fromUser.avatar  +"><div style=\"position:relative;top:-30px;left:5px;font-size:10px\" id=date>" + dateFr() + " " + heure() + " "+ jsonMessage.fromUser.name + ": </div><div style=\"position:relative;top:-10px;left:-13px;font-size:16px\" id=themessage>"+ jsonMessage.message +  "</div></div>");	
	}
	
	function sendToShare(jsonMessage)
	{
		
		$("#messageShareContent").val(jsonMessage.message);	
		$('#messageShareContent').removeClass().addClass('swing animated').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
		      $('#messageShareContent').removeClass("swing animated");
		    });
	}
	
	function sendToStatSystem(jsonMessage)
	{
		
		drawSystem(jsonMessage.param.free,jsonMessage.param.used,jsonMessage.param.thread);
		drawTodo(jsonMessage.param.stillToken,jsonMessage.param.totalToken,jsonMessage.param.running);
		drawUserStats(jsonMessage.param.users);
	}
	
	function sendAttribUser(jsonMessage)
	{
		attribServer(jsonMessage.message,jsonMessage.fromUser);
		drawUserStats(jsonMessage.param.users);
	}
	
	function sendState(jsonMessage)
	{
		if ( userJson.name == jsonMessage.fromUser.name)
			{
			console.log("Filtering because i'm the author, avoiding infinite loop, i'm " + userJson.name + " message is from " + jsonMessage.fromUser.name);
			} else
				{
				setState(jsonMessage.message);
				}
	}
	
	function sendComment(jsonMessage)
	{
		setComment(jsonMessage.message,jsonMessage.id);
	}
	
	
	function sendScript(jsonMessage)
	{
		setScript(jsonMessage.id,jsonMessage.message,jsonMessage.param.script,jsonMessage.param.rc);
	}
	
	
	var onMessage = function(event) {
		var data = event.data;
		var jsonMessage=JSON.parse(data);
		//console.log(jsonMessage);
		// Si message de type POSTMESSAGE, alors direction chat
		if ( jsonMessage.action == "POSTMESSAGE" )
			{
		    sendToBubble(jsonMessage);
			}else
						{
							console.log("MESSAGE not implemented  " + jsonMessage.action);
							}
		
		
	};
	
	var onError = function(event) {
		alert("Error : " + event.data);
	}
	
	

	WebSocketClient = {
			open: function (url,user)
			{
				serverUrl=url;
				open(url,user);
				
			},
			send: function (message)
			{
				//console.log("Really sending " + message);
				ws.send(message);
			}
			
		
	};
}
