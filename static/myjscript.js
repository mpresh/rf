


$(document).ready(function() {
	//$("#invite_popup").hide();
	$("#invite_popup").css("background-color","yellow");
	$("#invite_popup").css("width","400px");
	$("#invite_popup").css("height","800px");




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