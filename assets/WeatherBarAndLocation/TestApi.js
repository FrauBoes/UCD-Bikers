//location code taken from w3schools.com

//var x = document.getElementById("pos");

function getLocation() {
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else {
        document.getElementById("pos").innerHTML = "N/A";
    }
    
    
}

function showPosition(position) {
    document.getElementById("pos").innerHTML = "Latitude: " + position.coords.latitude +"<br>Longitude" +position.coords.longitude;
}

function resetVals() {
	var xmlhttp = new XMLHttpRequest();
	var url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=31f19a108384bc317e2d91c5621c791e";
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			//Parse the JSON data to a JavaScript variable. 
			var myArr = JSON.parse(xmlhttp.responseText);
			// This function is defined below and deals with the JSON data read from the file. 
			myFunction(myArr);
		}
	}
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
    
    function myFunction(obj) {
                
        var weather = obj.list[0].weather[0].icon;
        
        var temp = parseInt(obj.list[0].main.temp -273.15);
        
        var city = obj.city.name;
        
        var time = new Date();
        
        var hours = time.getHours();
        
        var rtime;
        
        if (hours>=0 && hours<3) {
            rtime=0;
        }
        else if (hours>=3 && hours<6) {
            rtime=3;
        }
        else if (hours>=6 && hours<9) {
            rtime=6;
        }
        else if (hours>=9 && hours<12) {
            rtime=9;
        }
        else if (hours>=12 && hours<15) {
            rtime=12;
        }
        else if (hours>=15 && hours<18) {
            rtime=15;
        }
        else if (hours>=18 && hours<21) {
            rtime=18;
        }
        else if (hours>=21 && hours<24) {
            rtime=21;
        }
        var disp1 ="<div class='icon'></div>";
        var disp2 ="";
        display = "<h1>"+weather+","+city+hours+"</h1>";
        var slot="";
        var j = 1;
        for (var i = 0; i < 6; i++) {
            
            if (rtime<10){
                slot = "0"+rtime+":00";
            }
            else {slot = rtime +":00";}
            rtime += 3;
            if (rtime>=24){
                rtime=0;
            }
//            if (rtime>12){
//                rtime-=12;
//                slot = rtime+"PM";
//            }
//            else {slot = rtime + "AM";}
//            rtime+=3;
                
            disp1 += "<div class='icon'><img class='img' src='icons/" + weather + ".png'>"+temp+"&#8451</div>";
            disp2 += "<div class='time'>"+slot+"</div>";

            temp = parseInt(obj.list[j].main.temp -273.15);
            weather = obj.list[j].weather[0].icon;
            j++;
        }
        disp2 += "<div class='time'></div>"
        
        document.getElementById("uWrap").innerHTML = disp1;
        document.getElementById("lWrap").innerHTML = disp2;
    }
}