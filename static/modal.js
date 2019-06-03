/*
TAPAHTUMAKARTTA
https://github.com/tapahtumakartta/tapahtumakartta-interface

Licensed under the
GNU General Public License v3.0

Description:
  HTML modal logic
*/

// Create handles to the DOM elements
// Response modal
var responseModal = document.getElementById("resModal");
// Response modal text area
var responseModalTxt = document.getElementById("resInfoArea");
// Response modal close button element
var responseModalCloseBtn = document.getElementsByClassName("close")[0];
// Share button
var shareButton = document.getElementsByClassName("button")[0];


// When the user clicks on the share button,
// open the response modal
function modalPopUp(data) {
  responseModal.style.display = "block";
  var hash_1 = document.getElementById("hash1");
  var hash_2 = document.getElementById("hash2");
  shareButton.style.display = "none";

  hash_1.innerHTML = data[0];
  hash_2.innerHTML = data[1];
}


// Close the modal
responseModalCloseBtn.onclick = function() {
  responseModal.style.display = "none";
  shareButton.style.display = "block";
}
window.onclick = function(event) {
  if (event.target == responseModal) {
    responseModal.style.display = "none";
    shareButton.style.display = "block";
  }
}
