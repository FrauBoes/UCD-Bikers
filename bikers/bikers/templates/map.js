
<script> 
// script to draw circle on the screen
function initMap(){
	// get the user's geolocation
	var cord;
	
	cord = {lat:53.3439118,lng:-6.2658777};
	
	var map=new google.maps.Map(document.getElementById('map'),{
		zoom:14,
		center:cord});
		
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
		setCenterAndList(position.coords.latitude, position.coords.longitude);
		
	}
	
	function setCenterAndList(lat,lng){
	console.log(location)
 	var xhttp = new XMLHttpRequest();
 	xhttp.onreadystatechange = function(){
 		if (this.readyState == 4 && this.status == 200){
 			console.log(this.reponseText);
 			var jsonText = this.responseText;
 			var array = JSON.parse(jsonText);
 			console.log(array)
 			document.getElementsByClassName("station-worddetails")[0].innerHTML = array[0];
 			document.getElementsByClassName("station-worddetails")[1].innerHTML = array[1];
 			document.getElementsByClassName("station-worddetails")[2].innerHTML = array[2];
 			//document.getElementById("station-1").innerHTML = array[1];
 			//document.getElementById("station-3").innerHTML = array[2];
 			var panormaslocations = [positions[array[0]],positions[array[1]],positions[array[2]]];
 			initPano(panormaslocations);
 			}
 		};
 	xhttp.open("GET","userlocation?lat="+lat+"&lon="+lng,true);
 	xhttp.send();
 }
 


	// get the data from the flask
	// it's not the ideal way to get data, just a test, will prove at the next level
	var positions = {{ locations | tojson | safe }};
	var number = {{ number }};
	var bike_stands = {{ bike_stands }};
	var available_bikes = {{ available_bikes }};
	var category = {{ category }};

	
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
	
	
	
	
	
//var markerCluster = new MarkerCluster(map,markers,{imagePath: "{{ url_for('static', filename='images/bike_stand.png') }}"});
  /*var circles = positions.map(function(location,i){
  	return new google.maps.Circle({
            strokeColor: changeColor(available_bikes[i],bike_stands[i]),
            strokeOpacity: 0.8,
            strokeWeight: 1,
            fillColor: changeColor(available_bikes[i],bike_stands[i]),
            fillOpacity: 0.5,
            map: map,
            center: positions[i],
            radius: bike_stands[i]*4,
            clickable: true,
  	});
  });*/
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
  		console.log(element.position["lat"]);
  		setCenterAndList(element.position['lat'],element.position["lng"]);
  		});
  });
  
	// Add a marker cluster tomanage the markers
	//var markerCluster = new MarkerClusterer(map,markers,{imagepath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'}); 
	
	}
	
 function loadMore(number){
 	var xhttp = new XMLHttpRequest();
 	xhttp.onreadystatechange = function(){
 		if (this.readyState == 4 && this.status == 200){
 			console.log(this.responseText);
 			//document.getElementById("occupancy-bar").innerHTML='';
 			//h1 = document.createElement("div");
 			//h1.innerHTML=this.responseText;
 			//document.getElementById("occupancy-bar").appendChild(h1);
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
