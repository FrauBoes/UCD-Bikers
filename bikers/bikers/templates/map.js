<script> 
// script to draw circle on the screen

function initMap(){
	// user's default location
	var cord = {lat:53.3439118,lng:-6.2658777};
	
	// init map instance
	var map=new google.maps.Map(document.getElementById('map'),{
		zoom:14,
		center:cord});
	
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
// 	 	var xhttp = new XMLHttpRequest();
// 	 	xhttp.onreadystatechange = function(){
// 	 		if (this.readyState == 4 && this.status == 200){
// 	 			var jsonText = this.responseText;
// 	 			var listDict = JSON.parse(jsonText);
// 	 			console.log(listDict)
// 	 			document.getElementsByClassName("station-worddetails")[0].innerHTML = listDict[0].toString();
// 	 			document.getElementsByClassName("station-worddetails")[1].innerHTML = listDict[1].toString();
// 	 			document.getElementsByClassName("station-worddetails")[2].innerHTML = listDict[2].toString();
// 	 			//document.getElementById("station-1").innerHTML = array[1];
// 	 			//document.getElementById("station-3").innerHTML = array[2];
// 	 			//var lsitCord = []
// 	 			//var values = Objest.keys()
// 	 			//var panormaslocations = Object.keys(listDict[0])
// 	 			//initPano(panormaslocations);
// 	 			}
// 	 		};
// 	 	xhttp.open("GET","userlocation?lat="+lat+"&lon="+lng,true);
// 	 	xhttp.send();
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

	/*function getlocation(){
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
 } */

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
<<<<<<< HEAD
 			//document.getElementById("occupancy-bar").innerHTML=this.responseText;
=======
>>>>>>> 57bb7c1c3163ce1108cc5f53b15323c14d0581f3
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
