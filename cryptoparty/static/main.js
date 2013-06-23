var map;
var marker;

$(document).ready(function () {
    var mapOptions = {
            zoom: 6, center: new google.maps.LatLng(48.37, 10.89),
            mapTypeId: google.maps.MapTypeId.ROADMAP 
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

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
