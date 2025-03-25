function getCSRFToken() {
  return document.querySelector('#save-form input[name=csrfmiddlewaretoken]').value;
}

function toggleSave(routeId) {
  fetch(`/routes/${routeId}/toggle-save/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
  .then(response => response.json())
  .then(data => {
    const icon = document.getElementById('save-icon');
    if (data.saved) {
      icon.classList.remove('bi-bookmark');
      icon.classList.add('bi-bookmark-fill');
    } else {
      icon.classList.remove('bi-bookmark-fill');
      icon.classList.add('bi-bookmark');
    }
  })
  .catch(err => console.error('Save toggle failed:', err));
}