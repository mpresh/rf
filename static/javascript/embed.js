function loadScript(url, callback){
 
    var script = document.createElement("script")
	script.type = "text/javascript";
 
    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState == "loaded" ||
		script.readyState == "complete"){
                script.onreadystatechange = null;
                callback();
            }
        };
    } else {  //Others
        script.onload = function(){
            callback();
        };
    }
 
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}

function loadjscssfile(filename, filetype){
    if (filetype=="js"){ //if filename is a external JavaScript file
	var fileref=document.createElement('script')
	    fileref.setAttribute("type","text/javascript")
	    fileref.setAttribute("src", filename)
	    }
    else if (filetype=="css"){ //if filename is an external CSS file
	var fileref=document.createElement("link")
	    fileref.setAttribute("rel", "stylesheet")
	    fileref.setAttribute("type", "text/css")
	    fileref.setAttribute("href", filename)
	    }
    if (typeof fileref!="undefined")
	document.getElementsByTagName("head")[0].appendChild(fileref)
	    }

loadjscssfile("http://code.jquery.com/jquery-1.4.2.min.js", "js");
loadjscssfile("/site_media/javascript/myjscript.js", "js");
loadjscssfile("/site_media/javascript/jquery.tools.min.js", "js");
loadjscssfile("/site_media/javascript/charCount.js", "js");
loadjscssfile("/site_media/javascript/jquery.cookie.js", "js");
loadjscssfile("/site_media/javascript/jquery.showLoading.js", "js");
loadjscssfile("/site_media/javascript/ZeroClipboard.js", "js");

loadjscssfile("/site_media/css/showLoading.css", "css");
loadjscssfile("/site_media/css/blueprint/typography.css", "css");
loadjscssfile("/site_media/css/overlayA.css", "css");
loadjscssfile("/site_media/css/landingA.css", "css");



alert("hello");