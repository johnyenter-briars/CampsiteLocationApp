function GetCampSitesWithinRadius()
{
    var data = JSON.parse(sessionStorage.getItem("LatandLong"));

    console.log(data);

    RequestCampsiteApiData(data);
}
function RequestCampsiteApiData(data)
{
    var apiurl = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + data.latitude + "," + data.longitude + "&key=AIzaSyB31C7CeNH_CyGtLBaKz7SlWLmgkLvB7kE"

    var request = new XMLHttpRequest();

    request.open('GET', apiurl, true);

    request.onload = function () {
        //console.log(this.response);
        sessionStorage.setItem('NearCampLocationData', JSON.stringify(this.response));
        //console.log("data")
        $.post( "/postmethod", {
            javascript_data: JSON.stringify(this.response)
        });
        var data = JSON.parse(this.response);
        console.log(data);
        console.log()
    }
    request.send();
}