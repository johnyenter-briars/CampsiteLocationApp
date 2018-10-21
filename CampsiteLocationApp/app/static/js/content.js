var map;

function initMap() {
	var lat_sw = 43.68042914325346
	var lng_sw= -70.6307728589731
	var lat_ne = 45.73738294592985
	var lng_ne = -66.51340783041827
	
	map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: (lat_ne + lat_sw)/2, lng: (lng_sw + lng_ne)/2},
	  zoom: 8
	});
	
	cpe = {lat: (lat_ne + lat_sw)/2, lng: (lng_sw + lng_ne)/2};
	
	pl = cpe;
	
	var marker = new google.maps.Marker({
	id: "positionmarker",
	position: cpe,
	map:map,
	draggable:true,
	label: "P"

	});
	var infowindow = new google.maps.InfoWindow({
	content: "Pickup Point"
	});

	google.maps.event.addDomListener(marker, 'dragend', function (event) {
		var lat = marker.position.lat();
		var lng = marker.position.lng();
		console.log("lat: " + lat);
		console.log("long: " + lng);
	});
}
