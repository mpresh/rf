


function make_friend_list(data) {
    html = "";
    $.each(data,function(i,list) {
	    html +=	friend_check_html(list["screen_name"],list["profile_image_url"],list["name"]);
	});
    return html;
}

function friend_check_html(namev,urlv,userv) {
    html = '<input type="checkbox" name="invitee" value='+userv+'  /><img src='+urlv+'/><span>'+namev+'</span><br />';
    return html;
}


