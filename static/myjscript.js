


$(document).ready(function() {
    
	$("#visual_map").hide();
	$("#show_map").html("(Show Map)");

	if (GBrowserIsCompatible()) {
	    var map = new GMap2(document.getElementById("visual_map"));
	    map.setCenter(new GLatLng(37.4419, -122.1419), 13);
	    map.setUIToDefault();
	}			


	$("#show_map").click(function() {

		if ($("#visual_img").is(":visible")) {

		    $("#visual_img").hide(500);
			
		    $("#visual_map").show(500, function() {
			   
			    if (GBrowserIsCompatible()) {
				var map = new GMap2(document.getElementById("visual_map"));
				map.setCenter(new GLatLng(37.4419, -122.1419), 13);
				map.setUIToDefault();
			    }
			});
		

		    $("#show_map").html("(Hide Map)");
		}else {
		    $("#visual_img").show(500);
		    $("#visual_map").hide(500);
		    $("#show_map").html("(Show Map)");
		}
	    });
			
		    
			

    });


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

