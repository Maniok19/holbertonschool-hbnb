/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  // Get the login form element
  const loginForm = document.getElementById('login-form');
  
  // Check if we're on the login page
  if (loginForm) {
    // Add submit event listener to the form
    loginForm.addEventListener('submit', async (event) => {
      // Prevent the default form submission
      event.preventDefault();
      
      // Get form data
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      
      try {
        // Send login request to API
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });
        
        // Parse the response data
        const data = await response.json();
        
        if (response.ok) {
          // Login successful - store JWT token in cookie
          document.cookie = `token=${data.access_token}; path=/; max-age=3600`; // 1 hour expiry (matching JWT_ACCESS_TOKEN_EXPIRES)
          
          // Store user info in localStorage if needed
          localStorage.setItem('isLoggedIn', 'true');
          
          // Redirect to the home page
          window.location.href = 'index.html';
        } else {
          // Login failed - show error message
          alert(`Login failed: ${data.error || 'Invalid credentials'}`);
        }
      } catch (error) {
        // Network or other error
        alert(`Error during login: ${error.message}`);
        console.error('Login error:', error);
      }
    });
  }
  
  // Check if user is logged in (can be used on any page)
  function isLoggedIn() {
    // Check for the token in the cookies
    return document.cookie.split(';').some(item => item.trim().startsWith('token='));
  }
  
  // Function to get the token from cookies
  function getToken() {
    const tokenCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('token='));
    return tokenCookie ? tokenCookie.split('=')[1] : null;
  }

  // Function to handle logout
  function logout() {
    // Clear the token cookie
    document.cookie = 'token=; path=/; max-age=0';
    // Clear localStorage
    localStorage.removeItem('isLoggedIn');
    // Redirect to login page
    window.location.href = 'login.html';
  }

  // Update header based on login status
  function updateHeader() {
    const loginLink = document.getElementById('login-link');
    
    if (loginLink) {
      if (isLoggedIn()) {
        // User is logged in, change to logout button
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.classList.remove('login-button');
        loginLink.classList.add('logout-button');
        loginLink.addEventListener('click', (e) => {
          e.preventDefault();
          logout();
        });
      } else {
        // User is not logged in, ensure it's a login link
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.classList.add('login-button');
        loginLink.classList.remove('logout-button');
      }
    }
  }

  // Add this if you need to check login status on page load
  if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname === '') {
    if (!isLoggedIn()) {
      // Redirect to login if not authenticated and on a protected page
      // You can comment this out if you want index.html to be accessible without login
      // window.location.href = 'login.html';
    }
  }

  // Update header on every page load
  updateHeader();
});