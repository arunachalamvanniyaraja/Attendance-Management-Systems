document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.json();
        if (result.status === 'success') {
            window.location.href = '/';
        } else {
            document.getElementById('error-message').textContent = result.message;
        }
    } catch (error) {
        document.getElementById('error-message').textContent = 'Login failed. Please try again.';
    }
});