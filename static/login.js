document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('form');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const username = loginForm.querySelector('#username').value;
        const password = loginForm.querySelector('#password').value;
        
        fetch('/login', {
            method: 'POST',
            body: JSON.stringify({ username: username, password: password }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/main'; // Redirect to main page after successful login
            } else {
                const errorDiv = document.createElement('div');
                errorDiv.textContent = 'Invalid username or password';
                errorDiv.style.color = 'red';
                loginForm.appendChild(errorDiv);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
