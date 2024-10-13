    include("static/javascript/jquery.js");
    include("static/javascript/jquery-ui.js")
    include("static/javascript/jquery-websocket.js")
    include("static/javascript/semantic.js")


    var popup;
    var ssPopup;
   
  
    function url(s) {
        var l = window.location;
        return ((l.protocol === "https:") ? "wss://" : "ws://") + l.hostname + (((l.port != 80) && (l.port != 443)) ? ":" + l.port : "") + "/" + s;
    }
    
    
    function buildJsonMessage(fromUser,message,action,id)
    {
    	var message={
    			fromUser: fromUser,
    			action: action,
    			message: message,
    			id: id
    	};
    	console.log(JSON.stringify(message));
    	return JSON.stringify(message);
    }

	function getValueFromActionGet(action,type) {
    	
		var retour;
		var request = $
				.ajax({
					url :  action,
					type : "GET",
					data : {},
					crossDomain: true,
					async : type,
					dataType : "html",
					error:function(xhr, status, errorThrown) {
					//alert("ERROR ! " + errorThrown+'\n'+status+'\n'+xhr.statusText);
					}
				});
		request.done(function(msg) {
			retour = trim(msg);
		});
		return retour;
	}
    
	/**
	 * Function Ajax
	 * @param theUrl
	 * @param asyncMode
	 * @returns
	 */
	function getValueFromUrl(theUrl,asyncMode,myfunction) {
		var retour; 
		try 
		{
		var request = $
				.ajax({
					url : theUrl,
					type : "GET",
					data : {},
					async : asyncMode,
					dataType : "html",
						error:function(xhr, status, errorThrown) {
//						alert("ERROR ! " + errorThrown+'\n'+status+'\n'+xhr.statusText);
							retour="ERROR";
				        } 
				});
				
		request
				.done(function(msg) {
					if ( typeof myfunction != "undefined" )
						{
						myfunction(msg);
						}else
							{
					retour = trim(msg);
							}
					
				});
				return retour;
				
	}	catch (err)
	{
		retour = "ERROR";
		return retour;
		}
	}
	
     // Quelques fonctions 
	function getValueFromAction(action,type,data) {

    	
		var retour;
		var request = $
				.ajax({
					url :  action,
					type : "POST",
					data : data,
					crossDomain: true,
					async : type,
					dataType : "html",
					error:function(xhr, status, errorThrown) {
					//alert("ERROR ! " + errorThrown+'\n'+status+'\n'+xhr.statusText);
					}
				});
		log("Transmission requête Ajax : " + 
				 action);
		request.done(function(msg) {
			log("Retour requête Ajax : " + msg);
			retour = trim(msg);
		});
		return retour;
	}
	
	 // Quelques fonctions 
	function getValueFromActionPost(action,type,data) {
    	
		var retour;
		var request = $
				.ajax({
					url :  action,
					type : "POST",
					method : "POST",
					data : "data=" + data,
					crossDomain: true,
					async : type,
					dataType : "html",
					error:function(xhr, status, errorThrown) {
					//alert("ERROR ! " + errorThrown+'\n'+status+'\n'+xhr.statusText);
					}
				});
		log("Transmission requête Ajax : " + 
				 action);
		request.done(function(msg) {
			log("Retour requête Ajax : " + msg);
			retour = trim(msg);
		});
		return retour;
	}
	
	
	function include(fileName){
		  document.write("<script type='text/javascript' src='"+fileName+"'></script>" );
		}
	
	function log(message)
    {
		var date = new Date();
    	console.log(message);
    	//console.log("LogMessage " + $("#LogMessage"));
    	//alert(date + " " + message +  "<br>" + $("#LogMessage").html());
    	$("#LogMessage").html( date + " " + message +  "<br>" + $("#LogMessage").html() );
    }
	function replaceAll(str,replace,with_this)
	{
	    var str_hasil ="";
	    var temp;

	    for(var i=0;i<str.length;i++) // not need to be equal. it causes the last change: undefined..
	    {
	        if (str[i] == replace)
	        {
	            temp = with_this;
	        }
	        else
	        {
	                temp = str[i];
	        }

	        str_hasil += temp;
	    }

	    return str_hasil;
	}
	function trim (myString)
    {
    return myString.replace(/^\s+/g,'').replace(/\s+$/g,'');
    } 
	
	
	function popupAddSimpleText(text,height,width)
    {
		$.modal(text);
    }
	
	function popupAdd(src,height,width)
    {
		popup=$.modal('<iframe src="' + src + '" height="' + (height-17) + '" width="' + (width -17) + '" style="position:fixed;border:0">', {
			closeHTML:"",
			
			containerCss:{
				border:0,
				height:height, 
				padding:0, 
				width:width
			},
			overlayClose:true
		});

    }
	
	function ssPopupAdd(src,height,width)
    {
		ssPopup=$.modal('<iframe src="' + src + '" height="' + (height-17) + '" width="' + (width -17) + '" style="position:fixed;border:0">', {
			closeHTML:"",
			
			containerCss:{
				border:0,
				height:height, 
				padding:0, 
				width:width
			},
			overlayClose:true
		});

    }
	
	function getUrlVars(url,cle)
	{
	    var vars = [], hash;
	    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
	    for(var i = 0; i < hashes.length; i++)
	    {
	        hash = hashes[i].split('=');
	        vars.push(hash[0]);
	        vars[hash[0]] = hash[1];
	    }
	    var valeur = vars[cle];
	    return valeur;
	}
	
	function deletePopup() {
	     //window.parent.document.getElementById('popup').style.display = 'none';
		 //alert("Suppression popup");
	     popup.close();
	     //$.modal.close();
	}
	
	function deleteSsPopup() {
	     //window.parent.document.getElementById('popup').style.display = 'none';
		 //alert("Suppression ssPopup");
	     ssPopup.close();
	     //$.modal.close();
	}

	function setUrl(url)
	{
		document.location=url;
	}
	
	function dateFr()
	{
	     // les noms de jours / mois
	     var jours = new Array("dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi");
	     var mois = new Array("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre");
	     // on recupere la date
	     var date = new Date();
	     // on construit le message
	     var message = jours[date.getDay()] + " ";   // nom du jour
	     message += date.getDate() + " ";   // numero du jour
	     message += mois[date.getMonth()] + " ";   // mois
	     message += date.getFullYear();
	     return message;
	}
	
	function heure()
	{
	     var date = new Date();
	     var heure = date.getHours();
	     var minutes = date.getMinutes();
	     if(minutes < 10)
	          minutes = "0" + minutes;
	     return heure + "h" + minutes;
	}
	
	
