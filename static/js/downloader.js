document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('downloadForm');
    const downloadBtn = document.getElementById('downloadBtn');
    const status = document.getElementById('status');
    const progressBar = document.querySelector('.progress');
    const progressBarInner = document.getElementById('progressBar');

    function showError(message) {
        status.className = 'alert alert-danger mt-3';
        status.style.display = 'block';
        status.textContent = message;
        downloadBtn.disabled = false;
        progressBar.style.display = 'none';
    }

    function showSuccess(message) {
        status.className = 'alert alert-success mt-3';
        status.style.display = 'block';
        status.textContent = message;
        downloadBtn.disabled = false;
        progressBar.style.display = 'none';
    }

    function showProgress() {
        status.style.display = 'none';
        progressBar.style.display = 'block';
        progressBarInner.style.width = '100%';
        downloadBtn.disabled = true;
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = document.getElementById('url').value.trim();
        
        if (!url) {
            showError('Please enter a valid URL');
            return;
        }

        showProgress();

        // Create a hidden form for the actual download
        const downloadForm = document.createElement('form');
        downloadForm.method = 'POST';
        downloadForm.action = '/download';

        const urlInput = document.createElement('input');
        urlInput.type = 'hidden';
        urlInput.name = 'url';
        urlInput.value = url;

        downloadForm.appendChild(urlInput);
        document.body.appendChild(downloadForm);

        // Submit the form
        downloadForm.submit();
        document.body.removeChild(downloadForm);

        // Reset the form and show success message
        setTimeout(() => {
            showSuccess('Download started! If it doesn\'t start automatically, click the download button again.');
            form.reset();
        }, 1000);
    });
});
