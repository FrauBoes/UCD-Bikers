<script> 
// script to draw circle on the screen

function initMap(){
	// user's default location
	var cord = {lat:53.3439118,lng:-6.2658777};
	
	// init map instance
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
	
	// init user location's marker
	var marker = new google.maps.Marker({
			position: cord,
			customInfo: "2",
			icon:{
			url: "{{ url_for('static', filename='images/self.png') }}",
			scaledSize: new google.maps.Size(64, 64)},
			map: map
		});
	
	// get user location and reset the map's center 
		//Get user location, if not, use the default location
	//If user's location between default location is greater than 2km, still use the default location 
	function getLocation(){
		if(navigator.geolocation){
			navigator.geolocation.getCurrentPosition(setMapCenter);
		}
	};
	
	function setMapCenter(position){ 
		//mark uers' locaiton with a marker
		//map.setCenter ({lat:position.coords.latitude, lng:position.coords.longitude });
		cord = {lat:position.coords.latitude, lng:position.coords.longitude };
		marker.setPosition(cord);
		setCenterAndList(position.coords.latitude, position.coords.longitude,initPano);
	}
	
	// with pure JAvascript to send query
	function setCenterAndList(lat,lng,func){
	 	var url = "userlocation?lat="+lat+"&lon="+lng;
	 	$.getJSON(url, function( data ) {
		  	 	document.getElementsByClassName("station-worddetails")[0].innerHTML = generateContent(data[0]);
	 			document.getElementsByClassName("station-worddetails")[1].innerHTML = generateContent(data[1]);
	 			document.getElementsByClassName("station-worddetails")[2].innerHTML = generateContent(data[2]);
	 			var i;
	 			var panoramalocations = [];
	 			for (i= 0; i<data.length;i++){
	 				document.getElementsByClassName("station-worddetails")[i].innerHTML = generateContent(data[i]);
	 				panoramalocations.push({lat: data[i]["lat"],lng: data[i]["lng"]})
	 			}
	 			func(panoramalocations);
	 				
		});
	}
	
	
	
	getLocation();

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

            bikerank(searchLat,searchLon);


    var url = "getstations?lng="+searchLon+"&lat="+searchLat
    $.getJSON(url, function(data)){

            station1 = data[0][1]
            station2 = data[1][1]
            station3 = data[2][1]
//            station4 = data[3]
//            station4 = data[4]


    }

          });
          map.fitBounds(bounds);
// Adapted from https://developers.google.com/maps/documentation/javascript/examples/places-searchbox


        });
	// get the data from the flask
	// it's not the ideal way to get data, just a test, will prove at the next level
	var positions = {{ locations | tojson | safe }};
	var number = {{ number }};
	var bike_stands = {{ bike_stands }};
	var available_bikes = {{ available_bikes }};
	var category = {{ category }};
	//var stationInfo = {{ stationInfo }};
	
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
	// for the street view part
	//panormaslocations= positions.slice(0, 3);
	function initPano(panormaslocations){
	var panoramas = panormaslocations.map(function(location, i){
		var id = "station-"+i.toString();
		console.log(id)
		var panorama = new google.maps.StreetViewPanorama(
			document.getElementById(id), {
				position: location,
				pov:{
					heading: 34,
					pitch: 10
				}
			}
		);
		map.setStreetView(panorama);
		return panorama
	});};
	
	//initPano(panormaslocations);
	
	function updatePano()
	
	
	

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
  		console.log(element.getPosition().lat());
  		console.log(element.position[0]);
  		console.log(element.position[1]);
  		setCenterAndList(element.getPosition().lat(),element.getPosition().lng());
  		});
  });

	}
	
 function loadMore(number){
 	var xhttp = new XMLHttpRequest();
 	xhttp.onreadystatechange = function(){
 		if (this.readyState == 4 && this.status == 200){
 			//document.getElementById("occupancy-bar").innerHTML=this.responseText;
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
 	str = '<h1> StationNO. '+respon.number.toString()+'  '+respon.name+ '</h1>';
 	str += '<p> Status: '+ respon.status + '</p>';
 	str += '<p> Address: '+ respon.address + '</p>';
 	str += '<p> Availible Bike: '+ respon.address + '</p>';
 	str += '<p> Bike Stands: '+ respon.address + '</p>';
 	
 	return str;
 	
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
