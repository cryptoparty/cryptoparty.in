var map;
var geocoder;

$(document).ready(function () {
    var mapOptions = {
            zoom: 1, center: new google.maps.LatLng(48.37, 10.89),
            mapTypeId: google.maps.MapTypeId.ROADMAP 
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    geocoder = new google.maps.Geocoder();


    // set default location if location is given in URL
    if(default_location != 'None') {
        geocoder.geocode({'address': default_location}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                map.setZoom(10);
            }
            else {
                console.log("geolocation error");
            }
        });
    }

    // get Cryptoparties for markers
    $.ajax({
        url: '/json/party',
        success: function(result) {
            parties = jQuery.parseJSON(result)
            $.each(parties, function(index, value) {
                var ll = new google.maps.LatLng(value.lat, value.lon);             
                var m = new google.maps.Marker({
                    position: ll,
                    map: map,
                    title: value.name});
                var i = new google.maps.InfoWindow({
                    content: '<p><h4>'+value.name+'</h4></p>'+
                             '<p><b>Street Address: </b>'+value.street_address+'</p>'+
                             '<p><b>Date: </b>'+value.time+'</p>'+
                             '<p><b>Additional Info: </b>'+value.additional_info+'</p>'+
                             '<p><b>Event Organizer: </b>'+value.organizer_email+'</p>'
                });
                google.maps.event.addListener(m, 'click', function() {
                    i.open(map, m);
                });
            });
        }
    });
});


// go to location

function map_go(address) {
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            map.setZoom(10);
        }
        else {
            console.log("geolocation error");
        }
    });
}

$('#search_location_go').on('click', function() {
    map_go($('#search_location_text').val());
});

$('#search_location_form').on('submit', function() {
    map_go($('#search_location_text').val());
    return false;
});


$('#subscription_search_btn').on('click', function() {
    var address = $('#subscription_location_text').val();
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            map.setZoom(10);
            $('[name=subscription_lat]').val(String(results[0].geometry.location.lat()));
            $('[name=subscription_lon]').val(String(results[0].geometry.location.lng()));
        }
        else {
            console.log("geolocation error");
        }
    });
    return false;
});

// submit subscription_form
$('#subscription_form').on('submit', function() {
    var formdata = {
        email: $('[name=subscription_email]').val(),
        lat: $('[name=subscription_lat]').val(),
        lon: $('[name=subscription_lon]').val()
    };

    $('#subscription_error').html("<div class=\"alert alert-info\">doing stuff...</div>");
    
    $.ajax({
        type: 'POST',
        url: '/json/subscription/add',
        data: {data: JSON.stringify(formdata)},
        success: function(result, status) {
            if(result == "OK") { 
                console.log(result);
                $('#subscription_error').html("<div class=\"alert alert-success\">"+
                    "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>"+
                    "<strong>Okay, then!</strong> You should receive a confirmation"+
                    "email shortly. Just click on the link in it and you're done!</div>")
            } else {
                $('#subscription_error').html("<div class=\"alert alert-error\">"+
                    "<strong>Oh no!</strong> Something was wrong. The server said: "+result+"</div>");
            }
        }
    });

    return false;
});

$('#addParty').on('show', function() {
    $('#add_party_iframe').attr('src', '/party/add');
});
