  /**
   * Navigation function for card sections
   */
  function navigateRoute(type, direction) {
     console.log(`navigateRoute triggered: type=${type}, direction=${direction}`);

    const container = document.querySelector(`.${type}-container`);
    const items = container.querySelectorAll(`.${type}-item`);
    const prevBtn = document.querySelector(`.${type}-prev`);
    const nextBtn = document.querySelector(`.${type}-next`);

    if (!items.length) return;

    let currentIndex = 0;
    items.forEach((item, index) => {
      if (!item.classList.contains('d-none')) {
        currentIndex = index;
      }
    });

    items[currentIndex].classList.add('d-none');
    let newIndex = (currentIndex + direction + items.length) % items.length;
    items[newIndex].classList.remove('d-none');

    prevBtn.disabled = items.length <= 1;
    nextBtn.disabled = items.length <= 1;
  }

  /**
   * Upload profile picture
   */
// Live preview profile image when a new file is selected
  const fileInput = document.getElementById('profile-photo-upload');
  const previewImg = document.getElementById('profile-preview');
  const profileForm = document.getElementById('profile-form');

  if (fileInput && previewImg && profileForm) {
    fileInput.addEventListener('change', function () {
      const file = this.files[0];
      if (!file) return;
       // Basic validation
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file(JPEG, PNG, etc.)');
        return;
      }

       // Check file size (e.g., 5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image must be less than 5MB');
        return;
      }

      // Create preview
 const reader = new FileReader();
    reader.onload = function(e) {
        // Show preview immediately
        document.getElementById('profile-preview').src = e.target.result;

        // Submit via AJAX
        const formData = new FormData(document.getElementById('profile-form'));

        fetch(window.location.href, {  // Or use profileForm.action
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // Critical for Django
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(data.message);
                // Optional: Update with server-processed URL
                if (data.profile_picture_url) {
                    document.getElementById('profile-preview').src = data.profile_picture_url;
                }
            } else {
                console.error("Error:", data.error);
            }
        })
        .catch(error => console.error("Network error:", error));
    };
    reader.readAsDataURL(file);
    });
  }