document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("comment-form");
  const messageBox = document.getElementById("comment-message");

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const url = form.action;

      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        }
      })
      .then(response => {
        if (response.headers.get("content-type").includes("application/json")) {
          return response.json();
        } else {
          throw new Error("Not a JSON response");
        }
      })
      .then(data => {
        if (data.success) {
          messageBox.textContent = data.message;
          messageBox.classList.remove('text-danger');
          messageBox.classList.add('text-success');
          messageBox.style.display = "block";

          form.reset();
        } else {
          messageBox.textContent = data.error || "Submission failed.";
          messageBox.classList.add('text-danger');
          messageBox.style.display = "block";
        }
      })
      .catch(error => {
        console.error("AJAX error:", error);
        messageBox.textContent = "Network or server error.";
        messageBox.classList.add('text-danger');
        messageBox.style.display = "block";
      });
    });
  }
});
