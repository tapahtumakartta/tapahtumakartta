/*
TAPAHTUMAKARTTA
https://github.com/tapahtumakartta/tapahtumakartta-interface

Licensed under the
GNU General Public License v3.0

Description:
  All the logic associated with the map functionality
*/

// Local REST API URI
const REST_API = "/rest/";

// Array for storing user-created markers
var markers = [];

// Set the initial center potision of the map
// Use the city of Jyväskylä with a really minimal zoom level so
// that the map of Finland is visible, if the user has denied
// the location promp
var initialCenter = [62.24147, 25.72088];
askLocation();

// Initiate the map
var map = L.map('map').setView(initialCenter, 6);

L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }
).addTo(map);


/* Sends pointer data to the backend server
 * Is called on button press
*/
function sendData() {
  var markerData = [];
  var markerTmp = {};

  // Simplify the list of markers by just saving the needed data
  for (item in markers) {
    markerTmp["title"] = markers[item].options.__proto__.title;
    markerTmp["desc"] = markers[item].options.__proto__.alt;
    markerTmp["lat"] = markers[item]._latlng.lat; // Coordinates
    markerTmp["lng"] = markers[item]._latlng.lng;

    // Save the temp object into the array
    markerData.push(markerTmp);
    markerTmp = {};
  }

  // Turn the marker array into a string
  var markerStr = JSON.stringify(markerData);

  // For debugging, show the number of markers
  console.log("Sending " + markerData.length + " markers");

  // Send the data to the backend
  var targetUri = REST_API + "new_map";
  httpMapDataAsync(targetUri, receiveResponse, "POST", markerStr);
  return;
}

/* Read search bar and parse it into an url to find new location */
function searchPlace() {
  var input = (document.getElementById("search-bar-field").value).replace(/ /g, "+");
  document.getElementById("search-bar-field").value = ""; // Clear input
  document.getElementById("search-bar-field").placeholder = ""; // Clear place holder
  var url = "https://nominatim.openstreetmap.org/search?q=" + input + "+finland&format=json&polygon=1&addressdetails=1";
  httpMapDataAsync(url, panMap, "GET"); // Query place and move map there
}

/* Read given json data and move map to coordinates found */
function panMap(json) {
  var data = JSON.parse(json);

  if (typeof data["0"] !== "undefined") { // Check if given data is valid
    var lat = data["0"]["lat"];
    var lon = data["0"]["lon"];
    map.panTo(new L.LatLng(lat, lon));
    }

  else{
    document.getElementById("search-bar-field").placeholder = "Place not found";
    }
}

/* Adds a marker to the Map
 * Is called on mouse click
 */
function addMarker(e) {
  var marker = L.marker(e.latlng).addTo(map);
  marker.on('click', function(){
    console.log(marker._latlng.lat);
    console.log(marker._latlng.lng);
  })
  markers.push(marker);
}

/* Get json data */
function httpMapDataAsync(theUrl, callback, method, data = null){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {

    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
    }

  xmlHttp.open(method, theUrl, true); // true for asynchronous

    // If data was provided, send it as a parameter
  if (data != null) {
    xmlHttp.send("q=" + data);
  } else {
    xmlHttp.send(null);
  }
}

/* Receives the data from an external resource */
function receiveResponse(response) {
  console.log(response);

  // Parse data for the user
  var responseObject = JSON.parse(response);
  var parsedResponse = "https://map.vey.cool/map/";
  parsedResponse += responseObject["user_hash"];
	// TODO: implement admin hash sharing here
	// and add necessary HTML stuff

  // Use the function from modal.js to open the
  // modal popup with the response information
  modalPopUp(parsedResponse);
  return;
}

/* Prompt for user geolocation and pan the map*/
function askLocation() {
  navigator.geolocation.getCurrentPosition(function(location) {
    map.panTo(new L.LatLng(location.coords.latitude, location.coords.longitude));
  });
}

/* Map event listeners
*/

map.on('click', addMarker); // add a marker onto the map
