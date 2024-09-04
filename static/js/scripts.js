
// CHECK IF password field === to repeated_password
function checkPasswordsMatch(password, repeatPassword, errorMessage) {
    if (password.value === repeatPassword.value) {
        errorMessage.style.display = 'none';
        return true; // Passwords match
    } else {
        errorMessage.style.display = 'block';
        return false; // Passwords do not match
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const repeatPassword = document.getElementById('repeat_password');
    const submitBtn = document.getElementById('submitBtn');
    const errorMessage = document.getElementById('error-message');

    submitBtn.addEventListener('click', function(event) {
        if (!checkPasswordsMatch(password, repeatPassword, errorMessage)) {
            event.preventDefault(); // Prevent form submission if passwords don't match
        }
    });
});