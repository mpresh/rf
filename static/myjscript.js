


$(document).ready(function() {
	//$("#invite_popup").hide();
	//$("#invite_popup").css("background-color","yellow");
	//$("#invite_popup").css("width","500px");
	//$("#invite_popup").css("height","300px");




	// MAP /IMAGE graphic
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



$(document).ready(function() {

$('#invite_popup_close').bind('click', function() {
    $('#invite_popup').hide();
   $('#twitlist').html("");
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




$(document).ready(function() {
$("#not_going_button").click(function(){
$.get('/ajax/event_not_going/{{event.id}}', function(data) {
location.reload();
});
});

$("#going_button").click(function(){
$.get('/ajax/event_going/{{event.id}}', function(data) {
location.reload();
});
});



$("#invite_button").overlay(
{
expose: {
loadSpeed: 200,
color: 'gray',
opacity: 0.8
}
}); 
    
});

function showbox() {
$('#invite_popup').show('slow');
$.getJSON('/ajax/event_friend_not_attendees/{{event.id}}', function(data){
$('#twitlist').append(make_friend_list(data));
});
}

