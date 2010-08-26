function ajaxFileUpload(file_name, success, campaign_id, image_purpose)
{
        $.ajaxFileUpload
	    (
	     {
		 url:'/upload_image?camp_id=' + campaign_id + '&file_name=' + file_name + '&image_purpose=' + image_purpose,
		     secureuri:false,
		     fileElementId:file_name,
		     dataType: 'json',
		     success: success,
		     error: function (data, status, e)
		     {
			 alert("error2 " + e);
		     }
	     }
	     )
 
	    return false;
 
}


function trim(stringToTrim) {
    return stringToTrim.replace(/^\s+|\s+$/g,"");
}

function inspect(obj, maxLevels, level)
{
  var str = '', type, msg;

    // Start Input Validations
    // Don't touch, we start iterating at level zero
    if(level == null)  level = 0;

    // At least you want to show the first level
    if(maxLevels == null) maxLevels = 1;
    if(maxLevels < 1)     
        return '<font color="red">Error: Levels number must be > 0</font>';

    // We start with a non null object
    if(obj == null)
    return '<font color="red">Error: Object <b>NULL</b></font>';
    // End Input Validations

    // Each Iteration must be indented
    str += '<ul>';

    // Start iterations for all objects in obj
    for(property in obj)
    {
      try
      {
          // Show "property" and "type property"
          type =  typeof(obj[property]);
          str += '<li>(' + type + ') ' + property + 
                 ( (obj[property]==null)?(': <b>null</b>'):('')) + '</li>';

          // We keep iterating if this property is an Object, non null
          // and we are inside the required number of levels
          if((type == 'object') && (obj[property] != null) && (level+1 < maxLevels))
          str += inspect(obj[property], maxLevels, level+1);
      }
      catch(err)
      {
        // Is there some properties in obj we can't access? Print it red.
        if(typeof(err) == 'string') msg = err;
        else if(err.message)        msg = err.message;
        else if(err.description)    msg = err.description;
        else                        msg = 'Unknown';

        str += '<li><font color="red">(Error) ' + property + ': ' + msg +'</font></li>';
      }
    }

      // Close indent
      str += '</ul>';

    return str;
}


function make_friend_list(data) {
    html = "";
    $.each(data,function(i,list) {
	    html +=	friend_check_html(list.name, list.profile_image_url, list.screen_name);
	});
    return "<ul id='friend_list'>" + html + "</ul>";
}


function friend_check_html(namev,urlv,userv) {
    html = '<li class="friend_list_item">&nbsp;&nbsp;<input type="hidden" name="invitee" value='+ userv +  ' /><img src="' + urlv + '"/>&nbsp;&nbsp;&nbsp;&nbsp;<span id="friend_name_text">'+namev+'</span><img class="checkbox_invite" src="/simpz/site_media/images/checkbox_unchecked.png" /></li>';

    return html;
}


function del_cookie(name) {
    document.cookie = name + '=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
}


function facebook_login_click() {
  var requiredPerms = ['email','user_about_me', 'publish_stream'];
  FB.login(function(response) {
	
    if (response.session) {
      var a = response.session;
      var options = { path: '/', expires: 10 };
      $.cookie("uid", a.uid, options);
      $.cookie("session_key", a.session_key, options);
      $.cookie("secret", a.secret, options);
      $.cookie("expires", a.expires, options);
      $.cookie("base_domain", a.base_domain, options);
      $.cookie("access_token", a.access_token, options);
      $.cookie("sig", a.sig, options);
  

      var url = "/facebook_callback?redirectArgs=overlayEQUALSfacebook";
      window.location.href = url;
  } else { FB.logout(function(response) { 
			}); }


      }, {perms: requiredPerms.join(',')}
      );

}



function smoothAdd(id, text)
{
    var el = $('#' + id);
    var h = el.height();

    el.css({
	    height:   h,
	    overflow: 'hidden'
	    });

    var ulPaddingTop    = parseInt(el.css('padding-top'));
    var ulPaddingBottom = parseInt(el.css('padding-bottom'));

    el.append('<li>' + text + '</li>');

    var first = $('li:first', el);
    var last  = $('li:last',  el);

    alert("first" + first);
    alert("last" + last);

    var foh = first.outerHeight();
    var heightDiff = foh - last.outerHeight();
    var oldMarginTop = first.css('margin-top');

    //first.css({
    //	    marginTop: 0 - foh,
    //		position:  'relative',
    //		top:       0 - ulPaddingTop
    //		});

    last.css('position', 'relative');

    alert(foh + "  " + oldMarginTop + "  " + h + "  "  + heightDiff);
    el.animate({ height: h + heightDiff }, 1500);

	//first.animate({ top: 0 }, 250, function() {
	//	first.animate({ marginTop: oldMarginTop }, 1000, function() {
	//		last.animate({ top: ulPaddingBottom }, 250, function() {
	//			//last.remove();
	//
	//			el.css({
	//				height:   'auto',
	//				    overflow: 'visible'
	//				    });
	//		});
	//	    });
	//    });
}