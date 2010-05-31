


function make_friend_list(data) {
    html = "";
    $.each(data,function(i,list) {
	    html +=	friend_check_html(list.name, list.profile_image_url, list.screen_name);
	});
    return "<ul id='friend_list'>" + html + "</ul>";
}


function friend_check_html(namev,urlv,userv) {
    html = '<li class="friend_list_item"><input type="checkbox" name="invitee" value='+ userv +  ' /><img src="' + urlv + '"/>&nbsp;&nbsp;&nbsp;&nbsp;<span id="friend_name_text">'+namev+'</span></li>';

    return html;
}

