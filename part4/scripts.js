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

    // Check authentication status when loading index page
    checkAuthentication();
    
    // Check if we're on the place details page
    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            const token = getCookie('token');
            fetchPlaceDetails(token, placeId);
        } else {
            displayError('No place ID specified');
        }
    }
    
    // Set up price filter event listener and populate options
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        // Clear existing options if any
        priceFilter.innerHTML = '';
        
        // Add the specified price filter options
        const options = [
            { value: '10', text: '$10' },
            { value: '50', text: '$50' },
            { value: '100', text: '$100' },
            { value: 'all', text: 'All' }
        ];
        
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            priceFilter.appendChild(optionElement);
        });
        
        // Set default selection to "All"
        priceFilter.value = 'all';
        
        // Add event listener
        priceFilter.addEventListener('change', handlePriceFilter);
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

// Function to get a cookie value by name
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}

// Function to check if user is authenticated
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

// Function to display error messages
function displayError(message) {
    alert(message); // Simple error display, could be improved with a dedicated error element
}

// Function to fetch places from API
async function fetchPlaces(token) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add token to headers if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch('http://localhost:5000/api/v1/places', {
            method: 'GET',
            headers: headers,
            credentials: 'include'
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            displayError('Failed to fetch places: ' + response.statusText);
        }
    } catch (error) {
        displayError('Error fetching places: ' + error.message);
    }
}

// Update the displayPlaces function in scripts.js
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
    
    // Clear loading message
    placesList.querySelector('h1').remove();
    
    // Get or create the cards container
    let cardsContainer = placesList.querySelector('.place_cards');
    if (!cardsContainer) {
        cardsContainer = document.createElement('div');
        cardsContainer.className = 'place_cards';
        placesList.appendChild(cardsContainer);
    } else {
        // Clear existing content
        cardsContainer.innerHTML = '';
    }
    
    // Store places data for filtering
    placesList.dataset.places = JSON.stringify(places);
    
    // Display each place
    places.forEach(place => {
        const placeElement = createPlaceElement(place);
        cardsContainer.appendChild(placeElement);
    });
}

// Helper function to create HTML for a place
function createPlaceElement(place) {
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place_card';
    placeDiv.dataset.price = place.price;
    
    placeDiv.innerHTML = `
        <img src="images/shrek_home.webp" alt="Place Image">
        <div class="card-content">
            <div>
                <h2>${place.title}</h2>
                <p class="price">$ ${place.price}</p>
            </div>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        </div>
    `;
    
    return placeDiv;
}

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: headers,
            credentials: 'include'
        });
        
        if (response.ok) {
            const placeDetails = await response.json();
            displayPlaceDetails(placeDetails);
        } else {
            displayError('Failed to fetch place details: ' + response.statusText);
        }
    } catch (error) {
        displayError('Error fetching place details: ' + error.message);
    }
}

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;
    placeDetailsSection.innerHTML = ''; // Clear existing content
    placeDetailsSection.innerHTML = `
             <div class="place_header">
                <h1 id="place-name">${place.title}</h1>
                <p id="place-location">${place.longitude}, ${place.latitude}</p>
             </div>
             <div class="place-info">
                <div class="place-main-info">
                    <div class="place-main-image">
                        <img id="place-main-image" src="images/shrek_home.webp" alt="Place image">
                    </div>
                    <div class="place-description">
                        <h2>Description</h2>
                        <p id="place-description-text">${place.description}</p>
                    </div>
                    <div class="place-details-sidebar">
                        <div class="place-price-info">
                            <h3>Price :</h3>
                            <p id="place-price">$ ${place.price}</p>
                            <p id="place-per-night">per night</p>
                        </div>
                        <div class="host-info">
                            <h3>Host</h3>
                            <div class="host-details">
                                <img src="images/shrek.jpg" alt="host-img">
                                <div>
                                    <p id="host-name">${place.owner.first_name}</p>
                                    <p id="host-since">Host since ${place.owner.created_at}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="place-amenities">
                        <!-- TO POPULATE-->
                        <h3>Amenities</h3>
                        <ul id="amenities-list">
                        ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
                        </ul>
                    </div>
                </div>
             </div>
    `;
}

// Function to handle price filtering
function handlePriceFilter(event) {
    const maxPrice = event.target.value;
    const placesList = document.getElementById('places-list');
    
    if (!placesList || !placesList.dataset.places) return;
    
    const places = JSON.parse(placesList.dataset.places);
    
    // Get the cards container
    let cardsContainer = placesList.querySelector('.place_cards');
    if (!cardsContainer) {
        cardsContainer = document.createElement('div');
        cardsContainer.className = 'place_cards';
        placesList.appendChild(cardsContainer);
    }
    
    // Clear existing content
    cardsContainer.innerHTML = '';
    
    // Filter and display places based on selected price
    places.forEach(place => {
        if (maxPrice === 'all' || parseInt(place.price || 0) <= parseInt(maxPrice)) {
            const placeElement = createPlaceElement(place);
            cardsContainer.appendChild(placeElement);
        }
    });
}

