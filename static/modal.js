/*
TAPAHTUMAKARTTA
https://github.com/tapahtumakartta/tapahtumakartta-interface

Licensed under the
GNU General Public License v3.0

Description:
  HTML modal logic
*/

// Get the modal
var modal = document.getElementById("resModal");
// Get the text area
var textArea = document.getElementById("resInfoArea");

// Get the close elements
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal 
function modalPopUp(data) {
  modal.style.display = "block";
  textArea.innerHTML = data;
}

// Close the modal
span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
