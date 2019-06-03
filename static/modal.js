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

// Close the modal
responseModalCloseBtn.onclick = function() {
  responseModal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == responseModal) {
    responseModal.style.display = "none";
  }
}
