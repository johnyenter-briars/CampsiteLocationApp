function GetCampSitesWithinRadius()
{
    var data = JSON.parse(sessionStorage.getItem("LatandLong"));

    RequestCurrentLocationData(data);
}
function RequestCurrentLocationData(data)
//Finds the state containing the coordinates in data
{
    var apiurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + data.latitude + "," + data.longitude + "&key=AIzaSyB31C7CeNH_CyGtLBaKz7SlWLmgkLvB7kE"

    var request = new XMLHttpRequest();

    request.open('GET', apiurl, true);

    request.onload = function () {
        //console.log(this.response);
        sessionStorage.setItem('NearCampLocationData', JSON.stringify(this.response));

        returndata = JSON.parse(this.response);

        var state = returndata.results[returndata.results.length-2].address_components[0].short_name;

        GetCampSiteAPIData(state, data);
    }
    request.send();
}

function GetCampSiteAPIData(state, location)
//Connects to campsite api based on the requested state
{
    var request = new XMLHttpRequest();

    var devkey = "8qmqjffpscjuwgqmmgcz3v84"

    var radius = 100;

    request.open('GET', "http://api.amp.active.com/camping/campgrounds/?pstate=" + state + "&api_key=" + devkey, true);

    request.onload = function () {
        $.post( "/api/search", {
            XMLCampsiteData: this.response, location: location.latitude + "," + location.longitude, radius: radius
        }).done(function(nearbycampsites){
            IterateThroughNearbyCampsites(nearbycampsites)
        });

    }
    request.send();
}

function IterateThroughNearbyCampsites(nearbycampsites)
{
    var bounds = new google.maps.LatLngBounds();
    var iframe = document.getElementById('MainMapiFrame');
    var innerDoc = iframe.contentDocument || iframe.contentWindow.document;
    var map = innerDoc.getElementById('map')

    var infoWindow = new google.maps.InfoWindow(), marker, i;

    $.each(nearbycampsites, function(index, val){
        //console.log(val);

        var position = new google.maps.LatLng(parseFloat(val.latitude), parseFloat(val.longitude));
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            setMap: map,
            title: val.facilityName[0],
            draggable:false,
            label: "T"
        });

        // Allow each marker to have an info window
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

    });

    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(14);
        google.maps.event.removeListener(boundsListener);
    });


}
function GetCampSitesNearCityState()
{
    var state = "CA"
    var city = "Mountain+View"

    var apiurl = "https://maps.googleapis.com/maps/api/geocode/json?address=" + city + "," + state + "&key=AIzaSyB31C7CeNH_CyGtLBaKz7SlWLmgkLvB7kE";

    var request = new XMLHttpRequest();

    request.open('GET', apiurl, true);

    request.onload = function () {
        var jsoneddata = JSON.parse(this.response);
        lat = jsoneddata.results[0].geometry.location.lat;
        lng = jsoneddata.results[0].geometry.location.lng;
        console.log(lat, lng);
        GetAPIDataWithMatchingCity(lat, lng, state)

    }
    request.send();
}

function GetAPIDataWithMatchingCity(lat, lng, state)
{
    var radius = 100

    var request = new XMLHttpRequest();

    var devkey = "8qmqjffpscjuwgqmmgcz3v84"

    var radius = 100;

    request.open('GET', "http://api.amp.active.com/camping/campgrounds/?pstate=" + state + "&api_key=" + devkey, true);

    request.onload = function () {
        $.post( "/api/search", {
            XMLCampsiteData: this.response, location: lat + "," + lng, radius: radius
        }).done(function(nearbycampsites){
            IterateThroughNearbyCampsites(nearbycampsites)
        });

    }
    request.send();

}
