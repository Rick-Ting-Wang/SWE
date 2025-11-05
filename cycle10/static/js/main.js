// Komodo Hub - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Dynamic form field interactions
    const orgTypeSelect = document.getElementById('org_type');
    if (orgTypeSelect) {
        orgTypeSelect.addEventListener('change', function() {
            const accessCodeField = document.getElementById('access_code');
            if (accessCodeField) {
                accessCodeField.style.display = this.value === 'private' ? 'block' : 'none';
            }
        });
    }

    // Toggle organization enrollment type
    const orgEnrollmentToggle = document.getElementById('is_org');
    if (orgEnrollmentToggle) {
        orgEnrollmentToggle.addEventListener('change', function() {
            const orgSelect = document.getElementById('org_id');
            if (orgSelect) {
                orgSelect.style.display = this.checked ? 'block' : 'none';
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Avatar preview functionality
    const avatarInput = document.getElementById('avatar');
    if (avatarInput) {
        avatarInput.addEventListener('change', function() {
            const preview = document.getElementById('avatar-preview');
            if (preview && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // Confirmation for destructive actions
    const deleteButtons = document.querySelectorAll('.btn-danger, [data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    console.log('Komodo Hub JavaScript loaded successfully');
});

// Utility functions
window.KomodoHub = {
    // Show loading state
    showLoading: function(element) {
        if (element) {
            element.disabled = true;
            const originalText = element.textContent;
            element.textContent = 'Loading...';
            element.setAttribute('data-original-text', originalText);
        }
    },

    // Hide loading state
    hideLoading: function(element) {
        if (element && element.hasAttribute('data-original-text')) {
            element.disabled = false;
            element.textContent = element.getAttribute('data-original-text');
        }
    },

    // Format date
    formatDate: function(dateString) {
        const options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return new Date(dateString).toLocaleDateString(undefined, options);
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
};