var geocoder;
		  var map;
		  function initialize() {
		    geocoder = new google.maps.Geocoder();
		    var latlng = new google.maps.LatLng(46.00, 2.00);
		    var mapOptions = {
		      zoom: 8,
		      center: latlng
		    }
		    map = new google.maps.Map(document.getElementById('map'), mapOptions);
		  }

		  function codeAddress() {
				function getReverseGeocodingData(lat, lng) {
				    var latlng = new google.maps.LatLng(lat, lng);
				    // This is making the Geocode request
				    var geocoder = new google.maps.Geocoder();
				    geocoder.geocode({ 'latLng': latlng }, function (results, status) {
				        if (status !== google.maps.GeocoderStatus.OK) {
				            alert(status);
				        }
				        // This is checking to see if the Geoeode Status is OK before proceeding
				        if (status == google.maps.GeocoderStatus.OK) {
				            //console.log(results);
				            var address = (results[0].formatted_address);
										//window.alert(address.toString());
				        }
				    });
				}
				//var position_user;
				var infoWindow = new google.maps.InfoWindow({map: map});
				if (navigator.geolocation) {
				 navigator.geolocation.getCurrentPosition(function(position) {

					 var pos = {
						 lat: position.coords.latitude,
						 lng: position.coords.longitude
					 };
					 //position_user=getReverseGeocodingData(pos.lat, pos.lng);
					 //window.alert(pos.lat);
					 //window.alert(pos.lng);
					 var pinColor = "0000FF";
						var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
								new google.maps.Size(21, 34),
								new google.maps.Point(0,0),
								new google.maps.Point(10, 34));
						var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
								new google.maps.Size(40, 37),
								new google.maps.Point(0, 0),
								new google.maps.Point(12, 35));
					var marker = new google.maps.Marker({
							map: map,
							position: pos,
							icon: pinImage,
							shadow: pinShadow,
							Title: "Votre position actuelle"
					 });
					 map.setCenter(pos);
					 //infoWindow.setPosition(pos);
					 //infoWindow.setContent('Votre localisation');
					 //map.setCenter(pos);
				 }, function() {
					 handleLocationError(true, infoWindow, map.getCenter());
				 });
			 } else {
				 // if Browser doesn't support Geolocation
				 handleLocationError(false, infoWindow, map.getCenter());
			 }
			 function handleLocationError(browserHasGeolocation, infoWindow, pos) {
				infoWindow.setPosition(pos);
				infoWindow.setContent(browserHasGeolocation ?
															'Error: The Geolocation service failed.' :
															'Error: Your browser doesn\'t support geolocation.');
			}
					var i=0;
					{% for objet in objets %}

						address = "{{objet.code_postal}}+{{objet.adresse}}";
						//position_user="6 avenue des arts 69100";
				    //var address = document.getElementById('address').value;
						//var distance = google.maps.geometry.spherical.computeDistanceBetween( "paris", "new_york" );
						//window.alert(distance);

					  geocoder.geocode( { 'address': address}, function(results, status) {
				      if (status == 'OK') {
								i=i+1;
				        //map.setCenter(results[0].geometry.location);

				        var marker = new google.maps.Marker({
				            map: map,
				            position: results[0].geometry.location,
										Title: "article n°"+i.toString()+" - {{objet.nom}}"
				        });
				      } else {
				        //alert('Geocode was not successful for the following reason: ' + status);
				      }
				    });
					{% endfor %}

		  }
