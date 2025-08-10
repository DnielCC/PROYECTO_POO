document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const switchToSignup = document.getElementById('switch-to-signup');
    const switchToLogin = document.getElementById('switch-to-login');

    // Function to switch to login form
    function showLoginForm() {
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
        
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        
        // Add slide animation
        loginForm.classList.add('slide-in');
        setTimeout(() => {
            loginForm.classList.remove('slide-in');
        }, 400);
    }

    // Function to switch to signup form
    function showSignupForm() {
        signupTab.classList.add('active');
        loginTab.classList.remove('active');
        
        signupForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        
        // Add slide animation
        signupForm.classList.add('slide-in');
        setTimeout(() => {
            signupForm.classList.remove('slide-in');
        }, 400);
    }

    // Event listeners for tabs
    loginTab.addEventListener('click', showLoginForm);
    signupTab.addEventListener('click', showSignupForm);

    // Event listeners for switch links
    switchToSignup.addEventListener('click', function(e) {
        e.preventDefault();
        showSignupForm();
    });

    switchToLogin.addEventListener('click', function(e) {
        e.preventDefault();
        showLoginForm();
    });

    // Form validation and submission
    const loginFormElement = document.getElementById('login-form');
    const signupFormElement = document.getElementById('signup-form');

    // Login form submission
    loginFormElement.addEventListener('submit', function(e) {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        if (!email || !password) {
            e.preventDefault();
            showError('Por favor completa todos los campos');
            return;
        }
        
        if (!isValidEmail(email)) {
            e.preventDefault();
            showError('Por favor ingresa un email válido');
            return;
        }
        
        // Form is valid, allow submission
    });

    // Signup form submission
    signupFormElement.addEventListener('submit', function(e) {
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        const confirmPassword = document.getElementById('signup-confirm-password').value;
        const name = document.getElementById('signup-name').value;
        
        if (!email || !password || !confirmPassword || !name) {
            e.preventDefault();
            showError('Por favor completa todos los campos');
            return;
        }
        
        if (!isValidEmail(email)) {
            e.preventDefault();
            showError('Por favor ingresa un email válido');
            return;
        }
        
        if (password.length < 6) {
            e.preventDefault();
            showError('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        if (password !== confirmPassword) {
            e.preventDefault();
            showError('Las contraseñas no coinciden');
            return;
        }
        
        // Form is valid, allow submission
    });

    // Email validation function
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Error display function
    function showError(message) {
        // Remove existing error messages
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Create new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 0.9rem;
            text-align: center;
            border: 1px solid #f5c6cb;
        `;
        errorDiv.textContent = message;
        
        // Insert error message at the top of the active form
        const activeForm = document.querySelector('.form:not(.hidden)');
        activeForm.insertBefore(errorDiv, activeForm.firstChild);
        
        // Auto-remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    // Add focus effects to inputs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });

    // Add loading state to buttons
    const buttons = document.querySelectorAll('.btn-primary');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                this.classList.add('loading');
                this.disabled = true;
                this.setAttribute('data-original-text', this.textContent);
                this.textContent = 'Procesando...';
                
                // Reset after form submission (or timeout)
                setTimeout(() => {
                    this.classList.remove('loading');
                    this.disabled = false;
                    this.textContent = this.getAttribute('data-original-text') || 'Continuar';
                }, 3000);
            }
        });
    });

    // Add smooth scroll for mobile
    if (window.innerWidth <= 768) {
        const container = document.querySelector('.container');
        container.style.scrollBehavior = 'smooth';
    }

    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            // Handle tab navigation
            const activeElement = document.activeElement;
            if (activeElement && activeElement.tagName === 'INPUT') {
                activeElement.parentElement.style.transform = 'translateY(-2px)';
            }
        }
    });

    // Add touch support for mobile
    if ('ontouchstart' in window) {
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(tab => {
            tab.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            tab.addEventListener('touchend', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
}); 