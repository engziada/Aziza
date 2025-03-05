/**
 * Main JavaScript file for the Dating Application
 * Contains client-side validation and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation for registration
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            const fullname = document.getElementById('fullname').value.trim();
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const phoneno = document.getElementById('phoneno').value.trim();
            
            // Validate fullname
            if (fullname.length < 3) {
                event.preventDefault();
                showError('Full name must be at least 3 characters long');
                return;
            }
            
            // Validate password
            if (password.length < 6) {
                event.preventDefault();
                showError('Password must be at least 6 characters long');
                return;
            }
            
            // Validate password confirmation
            if (password !== confirmPassword) {
                event.preventDefault();
                showError('Passwords do not match');
                return;
            }
            
            // Validate phone number format
            const phoneRegex = /^\d{10,15}$/;
            if (!phoneRegex.test(phoneno)) {
                event.preventDefault();
                showError('Please enter a valid phone number (10-15 digits)');
                return;
            }
        });
    }
    
    // Form validation for profile creation/update
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(event) {
            const age = document.getElementById('age').value;
            const gender = document.querySelector('input[name="gender"]:checked');
            
            // Validate age
            if (age && (age < 18 || age > 100)) {
                event.preventDefault();
                showError('Age must be between 18 and 100');
                return;
            }
            
            // Validate gender selection
            if (!gender) {
                event.preventDefault();
                showError('Please select a gender');
                return;
            }
        });
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                message.classList.add('fade-out');
                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 5000);
        });
    }
    
    // Helper function to show error messages
    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'flash-message error';
        errorDiv.textContent = message;
        
        const container = document.querySelector('.flash-container') || document.body;
        container.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            errorDiv.classList.add('fade-out');
            setTimeout(() => {
                errorDiv.remove();
            }, 500);
        }, 5000);
    }
    
    // Log to console for debugging
    console.log('Main.js loaded successfully');
    
    // Log the same message to the Logs folder
    logToFile('Main.js loaded successfully');
});

/**
 * Function to log messages to the console and to a file
 * @param {string} message - The message to log
 */
function logToFile(message) {
    console.log(message);
    
    // In a real implementation, you would use AJAX to send the log to the server
    // For now, we'll just log to the console
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}`;
    console.log(`Log entry: ${logMessage}`);
}
