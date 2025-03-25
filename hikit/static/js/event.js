document.addEventListener('DOMContentLoaded', function () {
  const commentForm = document.getElementById('comment-form');
  const commentSection = document.getElementById('comment-section');
  const messageBox = document.getElementById('comment-message');

  if (commentForm) {
    commentForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(commentForm);

      fetch(commentForm.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then((response) => {
          if (!response.ok) throw new Error('Network error');
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            // Append comment HTML to the section
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = data.comment_html;
            commentSection.prepend(tempDiv.firstElementChild);

            // Clear form
            commentForm.reset();

            // Optional: show success message
            messageBox.textContent = data.message;
            messageBox.style.display = 'block';
            messageBox.classList.remove('text-danger');
            messageBox.classList.add('text-success');
          } else {
            console.error('Comment error:', data.error);
            messageBox.textContent = 'Failed to post comment.';
            messageBox.classList.add('text-danger');
            messageBox.style.display = 'block';
          }
        })
        .catch((error) => {
          console.error('AJAX error:', error);
          messageBox.textContent = 'Network error';
          messageBox.classList.add('text-danger');
          messageBox.style.display = 'block';
        });
    });
  }
});
