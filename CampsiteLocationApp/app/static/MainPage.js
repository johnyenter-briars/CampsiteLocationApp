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
        $.post( "/postmethod", {
            XMLCampsiteData: this.response, location: location.latitude + "," + location.longitude, radius: radius
        });

    }
    request.send();
}