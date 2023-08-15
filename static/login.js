document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('form');
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const username = loginForm.querySelector('#username').value;
        const password = loginForm.querySelector('#password').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            window.location.href = '/main'; // Redirect to main page after successful login
        } else {
            const errorDiv = document.createElement('div');
            errorDiv.textContent = 'Invalid username or password';
            errorDiv.style.color = 'red';
            loginForm.appendChild(errorDiv);
        }
    });
});
