alert("sup");
$("#visual_map").hide();
$("#show_map").html("(Show Map)");

$(document).ready(function() {

	$("#visual_map").hide();
	$("#show_map").html("(Show Map)");

	
	$("#show_map").click(function() {
		


	   if ($("#visual_img").is(":visible")) {
		    $("#visual_img").hide(1000);
		    $("#visual_map").show(1000, create() {
			    if (GBrowserIsCompatible()) {
				var map = new GMap2(document.getElementById("visual_map"));
				map.setCenter(new GLatLng(37.4419, -122.1419), 13);
				map.setUIToDefault();
			    }});
		
		    $("#show_map").html("(Hide Map)");
		    alert("sup");
	   }else {
	       $("#visual_img").show(1000);
	       $("#visual_map").hide(1000);
	       $("#show_map").html("(Show Map)");
	       alert("sup");
	   }
	    }


	    )
	    });





$("#show_map").click(function() {
		


			if ($("#visual_img").is(":visible")) {
			$("#visual_img").hide(1000);
			$("#visual_map").show(1000, create() {
			if (GBrowserIsCompatible()) {
			var map = new GMap2(document.getElementById("visual_map"));
			map.setCenter(new GLatLng(37.4419, -122.1419), 13);
			map.setUIToDefault();
			}});
		
			$("#show_map").html("(Hide Map)");
			alert("sup");
			}else {
			$("#visual_img").show(1000);
			$("#visual_map").hide(1000);
			$("#show_map").html("(Show Map)");
			alert("sup");
			}
			}