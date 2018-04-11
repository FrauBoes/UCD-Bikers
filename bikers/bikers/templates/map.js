
<script>
// script to draw circle on the screen

function initMap(){
	// get the user's geolocation
	var cord;
	
	cord = {lat:53.3439118,lng:-6.2658777};
	
	var map=new google.maps.Map(document.getElementById('map'),{
		zoom:14,
		center:cord});

//	##################################################################################################

// Create the search box and link it to the UI element.
        var input = document.getElementById('place_search');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });



		
	var marker = new google.maps.Marker({
			position: cord,
		center:{lat:53.3439118,lng:-6.2658777}
	});
	
	var marker = new google.maps.Marker({
			position: {lat:53.3439118,lng:-6.2658777},
			customInfo: "2",
			icon:{
			url: "{{ url_for('static', filename='images/self.png') }}",
			scaledSize: new google.maps.Size(64, 64)},
			map: map
		});

	function getlocation(){
		console.log("getLocation")
		if(navigator.geolocation){
			navigator.geolocation.getCurrentPosition(setMapCenter);
		}
	}
	
	getlocation();

	//initialize the google map and set the center
	function setMapCenter(position){
		console.log(position)
		map.setCenter ({lat:position.coords.latitude, lng:position.coords.longitude });
		cord = {lat:position.coords.latitude, lng:position.coords.longitude };
		marker.setPosition(cord);
	}
	
searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
          });
          markers = [];

          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }
            var icon = {
              url: place.icon,
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));

            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }

            var searchLat = place.geometry.location.lat();
            var searchLon = place.geometry.location.lng();

          });
          map.fitBounds(bounds);
// Adapted from https://developers.google.com/maps/documentation/javascript/examples/places-searchbox


        });
	// get the data from the flask
	// it's not the ideal way to get data, just a test, will prove at the next level
	positions = {{ locations | tojson | safe }};
	number = {{ number }};
	bike_stands = {{ bike_stands }};
	available_bikes = {{ available_bikes }};
	category = {{ category }};

	
	var imagepath =["{{ url_for('static', filename='images/C0.png') }}",
	"{{ url_for('static', filename='images/C1.png') }}","{{ url_for('static', filename='images/C2.png') }}",
	"{{ url_for('static', filename='images/C3.png') }}","{{ url_for('static', filename='images/close.png') }}"]
	var markers = positions.map(function(location, i){
	
		var locationInfoWindow = new google.maps.InfoWindow({
			content:infoWindowContent(number[i])
		});
		return new google.maps.Marker({
			position: positions[i],
			customInfo: number[i].toString(),
			icon:{
			url: imagepath[category[i]],
			scaledSize: new google.maps.Size(64, 64)},
			map:map,
			infowindow:locationInfoWindow
		})
	});
	
	
	var imagepath =["{{ url_for('static', filename='images/C0.png') }}",
	"{{ url_for('static', filename='images/C1.png') }}","{{ url_for('static', filename='images/C2.png') }}",
	"{{ url_for('static', filename='images/C3.png') }}","{{ url_for('static', filename='images/close.png') }}"]
	var markers = positions.map(function(location, i){
	
		var locationInfoWindow = new google.maps.InfoWindow({
			content:infoWindowContent(number[i])
		});
		return new google.maps.Marker({
			position: positions[i],
			customInfo: number[i].toString(),
			icon:{
			url: imagepath[category[i]],
			scaledSize: new google.maps.Size(64, 64)},
			map:map,
			infowindow:locationInfoWindow
		})
	
	});
	

  var infoMark = false;
  markers.forEach(function(element){
  	// with query to request to the flask
  	
  	//var infowindow = new google.maps.InfoWindow({content: loadMore(element.label)});
  	element.addListener('click',function(){
  		console.log(element.customInfo);
  		hideAllInfoWindow(markers, map);
  		loadMore(element.customInfo);
  		element.infowindow.setPosition(element.position);
  		element.infowindow.open(map, element);
  		console.log(element.position.toString());
  		});
  });

	}
	
 function loadMore(number){
 	var xhttp = new XMLHttpRequest();
 	xhttp.onreadystatechange = function(){
 		if (this.readyState == 4 && this.status == 200){
 			console.log(this.responseText);
 			
 			var jsonText = this.responseText;
 			var array = JSON.parse(jsonText);
 			var data = google.visualization.arrayToDataTable(array);
 			chart.draw(data, options);
 			}
 		};
 	xhttp.open("GET","getdetail?num="+number,true);
 	xhttp.send();
 }
 
 
 function generateContent(respon){
 	//return "<div class='info'><h1>"+respon+"</h1></div>"
 }
 
 
 function infoWindowContent(content){
 	return "<p class='info'>"+content+'</p>'
 }
//function change color from red to blue
function changeColor(num,totalNum){
	var r,b;
	r = Math.round(255*(totalNum-num)/totalNum);
	b = Math.round(255*num/totalNum);
	color = "rgb("+r+",0,"+b+")";
	return color
}

function hideAllInfoWindow(markers,map){
	markers.forEach(function(marker){
		marker.infowindow.close(map,marker);
	});
}


</script>
