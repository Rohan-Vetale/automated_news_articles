// Show Bootstrap modal when form is submitted
document.getElementById('myForm').addEventListener('submit', function(event) {
  event.preventDefault();
  $('#successModal').modal('show');
});
