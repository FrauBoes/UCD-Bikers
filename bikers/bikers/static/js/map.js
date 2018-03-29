// script to draw circle on the screen
function initMap(){
	//initialize the google map and set the center
	var map=new google.maps.Map(document.getElementById('map'),{
		zoom:14,
		center:{lat:53.3458662,lng:-6.3066488}
	});
	// get the data from the flask
	// it's not the ideal way to get data, just a test, will prove at the next level
	positions = {{ locations | tojson | safe }};
	number = {{ number }};
	bike_stands = {{ bike_stands }}
	available_bikes = {{ availble_bikes }}
	
  var circles = positions.map(function(location,i){
  	return new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: positions[i],
            radius: bike_stands[i]
  	});
  });
  circles.forEach(function(element){
  	// with query to request to the flask
  	
  	//var infowindow = new google.maps.InfoWindow({content: loadMore(element.label)});
  	element.addListener('click',function(){
  		var infowindow = new google.maps.InfoWindow({
  		//content: loadMore(element.label)
  			content:element.center
  			});
  		infowindow.open(map, element)
  		});
  });
  
	// Add a marker cluster tomanage the markers
	//var markerCluster = new MarkerClusterer(map,markers,{imagepath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'}); 
	
	}
	
 function loadMore(number){
 	var xhhtp = new XMLHttpRequest();
 	xhttp.onreadystatechange = function(){
 		if (this.readyState == 4 && this.status == 200){
 			return generateContent(this.responseTex);
 			}
 		};
 	xhttp.open("GET","getdetail?num=number",true);
 	xhttp.send();
 }
 
 function generateContent(respon){
 	//return "<div class='info'><h1>"+respon+"</h1></div>"
 }
	

