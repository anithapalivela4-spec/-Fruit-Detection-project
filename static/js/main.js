/**
 * Fruit Disease Detection System - Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Image Drag & Drop and Preview Handler
    const dropZone = document.getElementById('upload-drop-zone');
    const fileInput = document.getElementById('image-file-input');
    const previewArea = document.getElementById('image-preview-area');
    const previewImg = document.getElementById('preview-img-element');
    const fileInfoText = document.getElementById('file-info-text');
    const removeBtn = document.getElementById('btn-remove-image');
    const submitBtn = document.getElementById('btn-submit-detection');

    if (dropZone && fileInput) {
        // Click drop zone triggers file input
        dropZone.addEventListener('click', function (e) {
            if (e.target !== removeBtn) {
                fileInput.click();
            }
        });

        // Dragover styling
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, function (e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, function (e) {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('dragover');
            }, false);
        });

        // Handle Drop
        dropZone.addEventListener('drop', function (e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                handleFileSelected(files[0]);
            }
        });

        // Handle File Input Change
        fileInput.addEventListener('change', function () {
            if (this.files && this.files.length > 0) {
                handleFileSelected(this.files[0]);
            }
        });

        function handleFileSelected(file) {
            const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'];
            if (!allowed.includes(file.type)) {
                alert('Invalid file format. Please select a JPG, JPEG, PNG, or WEBP image.');
                fileInput.value = '';
                return;
            }

            if (file.size > 10 * 1024 * 1024) {
                alert('File is too large. Maximum size allowed is 10 MB.');
                fileInput.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function (e) {
                if (previewImg) {
                    previewImg.src = e.target.result;
                }
                if (fileInfoText) {
                    const sizeKb = (file.size / 1024).toFixed(1);
                    fileInfoText.textContent = `${file.name} (${sizeKb} KB)`;
                }
                if (previewArea) {
                    previewArea.classList.remove('d-none');
                }
                dropZone.querySelector('.drop-zone-prompt')?.classList.add('d-none');
                if (submitBtn) {
                    submitBtn.removeAttribute('disabled');
                }
            };
            reader.readAsDataURL(file);
        }

        // Remove button handler
        if (removeBtn) {
            removeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                fileInput.value = '';
                if (previewArea) {
                    previewArea.classList.add('d-none');
                }
                dropZone.querySelector('.drop-zone-prompt')?.classList.remove('d-none');
                if (submitBtn) {
                    submitBtn.setAttribute('disabled', 'disabled');
                }
            });
        }
    }

    // 2. Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 6000);
    });

    // 3. Confirm Delete Prompts
    const deleteForms = document.querySelectorAll('.form-confirm-delete');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            if (!confirm('Are you sure you want to permanently delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
});
