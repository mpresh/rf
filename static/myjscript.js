


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


$(document).ready(function() {
    $("#header").click(function() {
        window.location = "/simpz/";
    });

    });

