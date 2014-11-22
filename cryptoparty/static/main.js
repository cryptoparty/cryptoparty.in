var map;

$(document).ready(function () {

    var ajaxRequest;
    var plotlist;
    var plotlayers = [];

    // set up the map
    map = new L.Map('map');
    var hash = new L.Hash(map);
    // create the tile layer with correct attribution
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib = 'Map data © OpenStreetMap contributors';
    var osm = new L.TileLayer(osmUrl, {
        minZoom: 0,
        maxZoom: 18,
        attribution: osmAttrib
    });

    map.setView(new L.LatLng(48.37, 10.89), 1);
    map.addLayer(osm);

    if (default_location != 'None') {
        map_go(default_location);
    }

    // get Cryptoparties for markers
    $.ajax({
        url: '/json/party',
        success: function (result) {
            parties = jQuery.parseJSON(result)
            $.each(parties, function (index, value) {
                var ll = new L.LatLng(value.position.coordinates[1], value.position.coordinates[0]);
                var ico = new L.Icon({iconUrl: value.organizer_avatar_url, iconSize: [48,48]});
                var marker = new L.Marker(ll, {icon: ico});
                if(value.organizer_twitter_handle != "") {
                    twitter_segment = '<p><b>Organizer\'s Twitter: </b><a href="https://twitter.com/' + value.organizer_twitter_handle + '">@'+value.organizer_twitter_handle     + '</a></p>';
                } else {
                    twitter_segment = '';
                }
                marker.bindPopup('<p><h4>' + value.name + '</h4></p>' + '<p><b>Street Address: </b>' + value.street_address + '</p>' + '<p><b>Date: </b>' + value.time + '</p><p><b>Description: </b>' + value.description + '</p><p><b>Additional Info: </b><a href="' + value.additional_info + '">[link]</a></p>' + '<p><b>Event Organizer: </b>' + value.organizer_email + '</p>' + twitter_segment);
                marker.addTo(map);
                               
            });
        }
    });

    });


// go to location

function map_go(search_string) {
    search_uri = encodeURI(search_string);
    $.ajax({
            url: 'http://nominatim.openstreetmap.org/search/'+ search_uri +'?format=json',
	    dataType: 'json',
            method: 'GET',
            success: function(result) {
                    locations = result;
                    lon = locations[0].lon;
                    lat = locations[0].lat;
                    console.log(lon+" "+lat);
                    target = new L.LatLng(locations[0].lat, locations[0].lon);
                    map.setView(target, 10);
            }
    });
}

$('#search_location_go').on('click', function () {
    console.log($('#search_location_text').val());
    map_go($('#search_location_text').val());
});

$('#search_location_form').on('submit', function () {
    map_go($('#search_location_text').val());
    return false;
});


$('#subscription_search_btn').on('click', function () {
    var address = $('#subscription_location_text').val();
    map_go(address);
    console.log(String(map.getCenter()));
    $('[name=subscription_lat]').val(String(map.getCenter().lat));
    $('[name=subscription_lon]').val(String(map.getCenter().lng));  
    return false;
});

// submit subscription_form
$('#subscription_form').on('submit', function () {
    var formdata = {
        email: $('[name=subscription_email]').val(),
        lat: $('[name=subscription_lat]').val(),
        lon: $('[name=subscription_lon]').val()
    };

    $('#subscription_error').html("<div class=\"alert alert-info\">doing stuff...</div>");

    $.ajax({
        type: 'POST',
        url: '/json/subscription/add',
        data: {
            data: JSON.stringify(formdata)
        },
        success: function (result, status) {
            if (result == "OK") {
                console.log(result);
                $('#subscription_error').html("<div class=\"alert alert-success\">" +
                    "<button type=\"button\" class=\"close\" data-dismiss=\"alert\">&times;</button>" +
                    "<strong>Okay, then!</strong> You should receive a confirmation " +
                    "email shortly. Just click on the link in it and you're done!</div>")
            } else {
                $('#subscription_error').html("<div class=\"alert alert-error\">" +
                    "<strong>Oh no!</strong> Something was wrong. The server said: " + result + "</div>");
            }
        },
        error: function (result, status) {
             $('#subscription_error').html("<div class=\"alert alert-error\">" +
                    "<strong>Oh no!</strong> Something was wrong. The server said: " + result + "</div>");
        },
    });

    return false;
});

$('#addParty').on('show', function () {
    $('#add_party_iframe').attr('src', '/party/add');
});
