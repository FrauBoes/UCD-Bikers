<script>
// Script so set up the map with station markers

function initMap(){

      // Iitialise the map station and center
      var mapInfo = {{ mapInfo | safe }};


      // User's default location
	  var cord = mapInfo.centerCord;


	  // Initialise map
	  var map=new google.maps.Map(document.getElementById('map'),{
		zoom:14,
		center:cord});

	  // Mark the user location with marker first
	  var userMarker = new google.maps.Marker({
			position: cord,
			customInfo: "2",
			icon:{
			url: "{{ url_for('static', filename='images/self.png') }}",
			scaledSize: new google.maps.Size(64, 64)},
			map: map
		});
		
	   /* Mark all the station Marker */
	   	  
	  // load all images which mark the different color
	  var imagepath =["{{ url_for('static', filename='images/C0.png') }}","{{ url_for('static', filename='images/C1.png') }}","{{ url_for('static', filename='images/C2.png') }}","{{ url_for('static', filename='images/C3.png') }}","{{ url_for('static', filename='images/close.png') }}"];

	  var numArray = Object.keys(mapInfo);

	  var infowindow = new google.maps.InfoWindow();

	  var markers = numArray.map(function(numStation, i){

        // Fetch all station coordinates
		var stationCord ={lat:mapInfo[numStation].lat,lng:mapInfo[numStation].lng};

		var marker = new google.maps.Marker({
			position: stationCord,
			customInfo: numStation,
			icon:{
			url: imagepath[mapInfo[numStation].category],
			scaledSize: new google.maps.Size(64, 64)},
			map: map,
		});

		// Reset map information based on the station that is clicked
		google.maps.event.addListener(marker, "click", function(){
			setGraph(marker.customInfo);
			setModel(marker.customInfo);
			setList(marker.position.lat(),marker.position.lng());
			//getPano(marker);
			clickedMarker = marker;
    		sv.getPanoramaByLocation(marker.getPosition(), 50, processSVData);
				//getPano(marker);
			});

		return marker
	 });

	// Create info window for each station
	var container = document.createElement("DIV");
	container.className = "container";
	container.style.width = "500px";
	container.style.height = "240px";
	var content = document.createElement("DIV");
	content.className = "row"
	container.appendChild(content);
	var streetview = document.createElement("DIV");
	streetview.style.width = "200px";
	streetview.style.height = "200px";
	streetview.className = "col-sm-6";
	content.appendChild(streetview);
	var htmlContent = document.createElement("DIV");
	htmlContent.className ="col-sm-6";
	content.appendChild(htmlContent);

	// Create the infowindow instance
	var infowindow = new google.maps.InfoWindow({content:content});

	var sv = new google.maps.StreetViewService();
	var clickedMarker = null;
	var pano = null;
	var pin = new google.maps.MVCObject();

   google.maps.event.addListenerOnce(infowindow, "domready", function(){
		pano = new google.maps.StreetViewPanorama(streetview, {
		    navigationControl: false,
		    enableCloseButton: false,
		    addressControl: false,
		    linksControl: false,
		    visible: true
  		});
		pano.bindTo("Position",pin);
   	});

  // Function to include street view wheel in window
  function processSVData(data, status) {
  if (status == google.maps.StreetViewStatus.OK) {
    var marker = clickedMarker;
    openInfoWindow(clickedMarker);

    if (!!pano && !!pano.setPano) {

      pano.setPano(data.location.pano);
      pano.setPov({
        heading: 270,
        pitch: 0,
        zoom: 1
      });
      pano.setVisible(true);

      google.maps.event.addListener(marker, 'click', function() {

        var markerPanoID = data.location.pano;
        // Set the Pano to use the passed panoID
        pano.setPano(markerPanoID);
        pano.setPov({
          heading: 270,
          pitch: 0,
          zoom: 1
        });
        pano.setVisible(true);
      });
    }
  } else {
    openInfoWindow(clickedMarker);
    title.innerHTML = clickedMarker.getTitle() + "<br>Street View data not found for this location";
    htmlContent.innerHTML = clickedMarker.myHtml;
    pano.setVisible(false);
  }
}


    // Function to open the window when a station is clicked
	function openInfoWindow(marker) {
 		htmlContent.innerHTML = generateInfoWindow(mapInfo[marker.customInfo]);
 		pin.set("position", marker.getPosition());
 		infowindow.open(map, marker);
		}

	// Get user's location
	getLocation();

    // Center map at user location
	// If user's location from default location is greater than 2km, still use the default location
	function getLocation(){
		if(navigator.geolocation){
			navigator.geolocation.getCurrentPosition(setUserMarker);
		}
	};

	function setUserMarker(position){
		// Mark user's location
		var cord = {lat:position.coords.latitude, lng:position.coords.longitude };
		userMarker.setPosition(cord);
		var lat = position.coords.latitude;
		var lng = position.coords.longitude;
		setMapCenter(lat,lng);
		setList(lat,lng);
	};

	// Function that sets map centre based on coordinates
	function setMapCenter(lat,lng){
		var url = "mapCenter?lat="+lat+"&lng="+lng;
		$.getJSON(url, function(data){
			map.setCenter(data.centerCord);
		})
	};

	// Calls function to find nearest 3 stations to coordinates
	function setList(lat,lng){
		var url = "list?lat="+lat+"&lng="+lng;
		$.getJSON(url, function(data){
			var i;
	 		for (i= 0; i<data.length;i++){
	 			generateContent(data[i],i);
	 		}
		})
	};

	// Refresh graph on event (load, resize or click)
    function setGraph(number){
	 	var url = "getGraph?num="+number;
	 	$.getJSON(url, function(data){
	 		var graphdata = google.visualization.arrayToDataTable(data);
	 	    chart.draw(graphdata, options);
	 	    });
	};
	
   function setModel(number){
	 	var url = "getModel?num="+number;
	 	$.getJSON(url, function(data){
	 		var graphdata = google.visualization.arrayToDataTable(data);
	 	    chartModel.draw(graphdata, optionsModel);
	 	    });	
	};


// Create the search box and link it to the UI element.
        var input = document.getElementById('place_search');
        var searchBox = new google.maps.places.SearchBox(input);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', function() {
          searchBox.setBounds(map.getBounds());
        });


// Process input from search box
searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }
		  spotmarkers = [];
          // Clear out the old markers.
          spotmarkers.forEach(function(marker) {
            marker.setMap(null);
          });

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
            spotmarkers.push(new google.maps.Marker({
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

            setList(searchLat, searchLon);

     });
             map.fitBounds(bounds);
// Adapted from https://developers.google.com/maps/documentation/javascript/examples/places-searchbox


        });

  var infoMark = false;}


 // Generate HTML for suggested stations
function generateContent(respon,i){
	$('.title').eq(i).html('NO.   '+respon.number.toString());
	$('.subtitle').eq(i).html(respon.address);
	$('.status').eq(i).html(respon.status);
	$('.bikes').eq(i).html(respon.availible_bike);
	$('.spaces').eq(i).html(respon.availible_space);
 }

 // Generate HTML for station info window
 function generateInfoWindow(respon){
 	str = '<h5> Station NO. '+respon.number.toString()+'</h5>'
 	str += '<h6>'+respon.name+ '</h6>';
 	str += '<p style ="text-align:left"> Status: '+ respon.status + '</p>';
 	str += '<p style ="text-align:left"> Availible Bikes: '+ respon.availible_bike + '</p>';
 	str += '<p style ="text-align:left"> Bike Stands: '+ respon.bike_stands+ '</p>';
 	str += '<p style ="text-align:left"> Avalible Space: '+respon.availible_space+ '</p>';
 	return str;

 }

</script>