document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get email and password from form
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                await loginUser(email, password);
            } catch (error) {
                displayError(error.message || 'An error occurred during login');
            }
        });
    }
});

async function loginUser(email, password) {
    // You'll need to replace this with your actual API endpoint
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
    });

    if (response.ok) {
        const data = await response.json();
        const expiryDate = new Date();
        expiryDate.setDate(expiryDate.getDate() + 7); // Cookie expires in 7 days
        
        // Set the cookie without Secure flag if on localhost (for development)
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const cookieString = `token=${data.access_token}; path=/; expires=${expiryDate.toUTCString()}; SameSite=Lax${isLocalhost ? '' : '; Secure'}`;
        document.cookie = cookieString;
        window.location.href = '/index.html';
    } else {
      alert('Login failed: ' + response.statusText);
  }
}