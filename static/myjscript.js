




function make_friend_list(data) {
    html = "";
    $.each(data,function(i,list) {
	    html +=	friend_check_html(list[0],list[1],list[2]);
	});
    return html;
}

function friend_check_html(namev,urlv,userv) {
    html = '<input type="checkbox" name="invitee" value='+userv+'  /><img src='+urlv+'/><span>'+namev+'</span><br />';
    return html;
}





function showbox() {
    $('#invite_popup').show('slow');
    $.getJSON('/ajax/event_friend_not_attendees/{{event.id}}', function(data){
	    $('#twitlist').append(make_friend_list(data));
	});
}

