//alert("embed");
$(".hiding").hide();
$(".showing").show();


// Global vars
var contentView = 0;
var shareLink = '';
var overlayType = 'twitter';
//
//alert("here i am");
FB.init({appId: facebook_app_id, status: true, cookie: true, xfbml: true});
//alert("hi2 facebook loaded OK");
 

FB.getLoginStatus(function(response) {
  if (response.session) {
    // logged in and connected user, someone you know
    $("#div-facebook-logged-in").show();
    $("#div-facebook-logged-out").hide();

    // if the user is logged in but has no fbuser, get it with ajax
    $.ajax({ 
                   url: facebook_sync_server_url,
    	           dataType: "json", 
    	           data: {uid : response.session.uid,
                          access_token : response.session.access_token},
    	           success: function (data){ 
                   },
    	           beforeSend: function() {
                 } 
    
        });

  } else {
    // no user session available, someone you dont know
    $("#div-facebook-logged-out").show();
    $("#div-facebook-logged-in").hide();
  }
});

/////////// twitter login ////////////////
$('#twitter-login').click(function(){
        var keyValuePairs = document.cookie.split(';');
       signinWin = window.open(tauth_login_url + "?popup=true", "SignIn", "width=780,height=410");
       setTimeout(CheckLoginStatusTwitter, 2000);
       signinWin.focus();
       return false;
});
function CheckLoginStatusTwitter() {
    if (signinWin.closed) {
        $.ajax({ 
            url: ajax_check_twitter_logged_in,
    	    dataType: "json", 
    	    data: {},
    	    success: function (data) {
		    //alert(JSON.stringify(data));
		    if (data["status"] == "1") {
    	               $("#div-twitter-logged-in").show();
                       $("#div-twitter-logged-out").hide();	
                       shareLink = 'twitter';
                       overlayType = "twitter";
                       $("#overlay-blogger-login").overlay().load();
		    }
		},			       
    	         beforeSend: function() {
                 } 
    	
    		
    	    });
    }
   else {
       setTimeout(CheckLoginStatusTwitter, 1000);
   }
}

///////////// facebook login //////////////
$('#facebook-login').click(function(){
	alert("https://graph.facebook.com/oauth/authorize?client_id=" + facebook_api + "&redirect_uri=" + redirect_uri + "&display=popup&scope=" + scope, "SignIn", "width=780,height=410");
       signinWin = window.open("https://graph.facebook.com/oauth/authorize?client_id=" + facebook_api + "&redirect_uri=" + redirect_uri + "&display=popup&scope=" + scope, "SignIn", "width=780,height=410");
       setTimeout(CheckLoginStatusFacebook, 2000);
       signinWin.focus();
       return false;
});
function CheckLoginStatusFacebook() {
    if (signinWin.closed) {

$.ajax({ 
            url: ajax_check_facebook_logged_in,
    	    dataType: "json", 
    	    data: {},
    	    success: function (data) {
	    //alert(JSON.stringify(data));
                if (data["status"] == "1") {
                   $("#div-facebook-logged-in").show();
                   $("#div-facebook-logged-out").hide();
                   shareLink = 'facebook';
                   overlayType = "facebook";
                   $("#overlay-blogger-login").overlay().load();
		}
		},			       
    	         beforeSend: function() {
                 } 
    	
    		
    	    });

    
    }
    else setTimeout(CheckLoginStatusFacebook, 1000);
}

////default usage
$("#overlay-textarea-twitter").charCount();
({
	allowed: 80,		
	warning: 20
});
$("#overlay-textarea-facebook").charCount();
({
	allowed: 80,		
	warning: 20
});



$('#flogout').click(function(){
        $.ajax({ 
                   url: ajax_facebook_logout_url,
	           dataType: "json", 
	           data: {},
	           success: function (data) { 
                       $("#div-facebook-logged-out").show();
                       $("#div-facebook-logged-in").hide();
                   },
	           beforeSend: function() {
       
                       var options  = { path: '/', expires: -1 };
	               $.cookie("uid", null, options);
	               $.cookie("session_key", null, options);
	               $.cookie("secret", null, options);
	               $.cookie("expires", null, options);
	               $.cookie("base_domain", null, options);
	               $.cookie("access_token", null, options);
	               $.cookie("sig", null, options);
                       FB.logout();

                 } 

        }); 
});

$('#tlogout').click(function(){
        $.ajax({ 
                   url: tauth_logout_url,
	           dataType: "json", 
	           data: {user_id: user_id},
	           success: function (data) {
                       user_id = '';
                       user = false;
                       $("#div-twitter-logged-out").show();
                       $("#div-twitter-logged-in").hide();    
                   },
	           beforeSend: function() {
                 } 

        }); 
});

function activateCopy() {
    ZeroClipboard.setMoviePath(clipboard_url ); 
    var clip = new ZeroClipboard.Client();
    clip.setText(code);
    clip.glue( 'd_clip_button', 'd_clip_container' );
}

$("#facebook-feed-update").click(function(){
	// Show discount page
	pageOverlay(3, '');
	//activateCopy();
	$.ajax({
		url: facebook_update_id_url, 
		dataType: "json",
		data: {message: $("#overlay-textarea-facebook").val(), 
			shash: shash,
			parent_url: parent_url},

		success: function(data){
                  refreshAttendee(15);
		},
		beforeSend: function() {
                if (campaign_type == "discount") 
                $("#code").showLoading({'afterShow': function(){ setTimeout( "jQuery('#code').hideLoading()", 3000 );}});         
                }
		});
});   

$("#twitter-feed-update").click(function() { 
        // Show discount page
        pageOverlay(3, '');
	//activateCopy();

	$.ajax({ 
                   url: campaign_tweet_invite_url, 
	           dataType: "json", 
	           data: {message: $("#overlay-textarea-twitter").val(), 
			shash: shash,
			parent_url: parent_url},
	           success: function (data) {
                                          $.get(campaign_going_twitter_url, 
	                                  function(data) { refreshAttendee(15); }); },
	           beforeSend: function() { 
                if (campaign_type == "discount") { 
                         $("#code").showLoading({'afterShow': function(){ setTimeout( "jQuery('#code').hideLoading()", 3000 );}});         
                }
                 } 

	    });
    }); 

$("#overlay-blogger-login").overlay({
	expose: {
		loadSpeed: 100,
		color: '#666',
		opacity: 0.0
	},
	onLoad: function(event) {
                // Which page to start on?
		// if twitter user logged in, show twitter page
		if (user && overlayTwitter) {
		    pageOverlay(2, 'twitter');
		}
                else {
	
		    // if fbuser logged in
		    if (fbuser && overlayFacebook) {
		        pageOverlay(2, 'facebook');
		    }
                    else {
	
		        // show first view with facebook and twitter login buttons
		        if (!user && !fbuser) {
		            pageOverlay(1, '');
		        }
                        else {
		        
		            // if fbuser logged in
		            if (fbuser) {
		                pageOverlay(2, 'facebook');
		            }
                            else { 	
		            
		                // if fbuser logged in
		                if (user) {
		                pageOverlay(2, 'twitter');
		                }
		            }
		        }
		    }
		}
            
		if (shareLink == 'facebook') {
		    pageOverlay(2, 'facebook');
		    shareLink = '';
		}
		if (shareLink == 'twitter') {
		    pageOverlay(2, 'twitter');
		    shareLink = '';
		}

	},
	top: 0,
	left: 3
});

function pageOverlay(page, type){
    type = overlayType;
    switch(page) 
    {
    case 1:
	contentView = 1;
        $('#overlay-div-content2-facebook').hide();
        $('#overlay-div-content2-twitter').hide();
        $('#overlay-div-content3').show();
	break;
    case 2:
        contentView = 2;
	if (type == 'facebook') {
	    $('#overlay-div-content2-facebook').show();
	    $('#overlay-div-content2-twitter').hide();
	    $('#overlay-div-content3').hide();
	} else {
	    $('#overlay-div-content2-facebook').hide();
	    $('#overlay-div-content2-twitter').show();
	    $('#overlay-div-content3').hide();
	}
	break;
    case 3:
        contentView = 3;
        $('#overlay-div-content2-facebook').hide();
        $('#overlay-div-content2-twitter').hide();
        $('#overlay-div-content3').show();
	break;
    default:
        break;
    }
}
$('#facebook-share').click(function(){
    shareLink = 'facebook';
    overlayType = "facebook";
    $("#overlay-blogger-login").overlay().load();
});

$('#twitter-share').click(function(){
    overlayType = "twitter";
    shareLink = 'twitter';
    $("#overlay-blogger-login").overlay().load();
});

