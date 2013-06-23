var map;
var geocoder;

$(document).ready(function () {
    var mapOptions = {
            zoom: 1, center: new google.maps.LatLng(48.37, 10.89),
            mapTypeId: google.maps.MapTypeId.ROADMAP 
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    geocoder = new google.maps.Geocoder();

    // get Cryptoparties for markers
    $.ajax({
        url: '/json/party',
        success: function(result) {
            parties = jQuery.parseJSON(result)
            $.each(parties, function(index, value) {
                var ll = new google.maps.LatLng(value.lat, value.lon);             
                m = new google.maps.Marker({
                    position: ll,
                    map: map,
                    title: value.name});
                i = new google.maps.InfoWindow({
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

function map_go() {
    var address = $('#search_location_text').val();
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

$('#search_location_go').on('click', map_go);

$('#search_location_form').on('submit', function() {
    map_go();
    return false;
});
