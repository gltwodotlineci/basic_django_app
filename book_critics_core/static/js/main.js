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


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function send_ticket_id(ticketId, dialog_id){

  fetch('http://localhost:8000/send_tc/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    credentials: 'include',
    body: JSON.stringify({ ticket_id: ticketId })
  })
  .then(res => res.json())
  .then(data => console.log('Success:', data))
  .catch(err => console.error('Error:', err));
  openDialogBox(dialog_id)

}
