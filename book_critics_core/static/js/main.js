// searching for the user
function searchUser() {
    var input = document.getElementById("searchInput");
  
    input.addEventListener("keyup", function(event) {
      var inputValue = event.target.value;
  
      if (inputValue.length > 0) {
        fetch('https://example.com/api/endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ value: inputValue }) // Send inputValue in the body
        })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
      }
    });
  }


function openDialogBox(id){
  var dialog = document.getElementById(id);
  if (dialog) {
    dialog.showModal();
  }
}

function closeDialogBox(id){
  var dialog = document.getElementById(id);
  if (dialog) {
    dialog.close();
  }
}
