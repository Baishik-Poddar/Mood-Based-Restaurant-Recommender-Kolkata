document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const moodInput = document.getElementById('mood');
    const moodButtons = document.querySelectorAll('.mood-option');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    
    // Use same origin when served by FastAPI (Docker/local server); fall back for file://
    const API_BASE_URL = window.location.protocol === 'file:'
        ? 'http://127.0.0.1:8000'
        : window.location.origin;

    // Check if the API server is running
    fetch(`${API_BASE_URL}/moods`)
        .then(response => {
            if (!response.ok) {
                throw new Error('API server is not accessible');
            }
            return response.json();
        })
        .then(data => {
            console.log('Connected to API server successfully');
        })
        .catch(error => {
            console.error('Error connecting to API:', error);
            resultsDiv.innerHTML = `
                <div class="col-12 text-center">
                    <div class="alert alert-danger">
                        <h4>Error connecting to API server</h4>
                        <p>Please make sure the server is running at ${API_BASE_URL}</p>
                        <p>Run: <code>uvicorn app.main:app --reload</code> in your terminal</p>
                    </div>
                </div>
            `;
        });

    // Set up mood buttons
    moodButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedMood = this.getAttribute('data-mood');
            moodInput.value = selectedMood;
            
            // Update active button style
            moodButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const mood = moodInput.value;
        const location = document.getElementById('location').value;
        const priceRange = document.getElementById('priceRange').value;

        if (!mood) {
            alert('Please enter your mood or select one from the options');
            return;
        }

        // Prepare data for both API call and URL parameters
        const requestData = {
            mood: mood.toLowerCase(),
            location: location || undefined,
            price_range: priceRange || undefined
        };
        
        // Create URL parameters for the results page
        const urlParams = new URLSearchParams();
        urlParams.append('mood', requestData.mood);
        if (location) urlParams.append('location', location);
        if (priceRange) urlParams.append('price_range', priceRange);
        
        // Show loading spinner
        loadingDiv.classList.remove('d-none');
        resultsDiv.innerHTML = '';
        
        // Make API request
        fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.detail || 'Something went wrong');
                });
            }
            return response.json();
        })
        .then(restaurants => {
            // Hide loading spinner
            loadingDiv.classList.add('d-none');
            
            // Store restaurant data in localStorage to access it from the results page
            localStorage.setItem('restaurantResults', JSON.stringify(restaurants));
            
            // Open results in a new tab
            window.open(`results.html?${urlParams.toString()}`, '_blank');
        })
        .catch(error => {
            console.error('Error:', error);
            loadingDiv.classList.add('d-none');
            resultsDiv.innerHTML = `
                <div class="col-12 text-center">
                    <div class="alert alert-danger">
                        <h4>Error</h4>
                        <p>${error.message || 'Sorry, something went wrong. Please try again later.'}</p>
                    </div>
                </div>
            `;
        });
    });

    function createRestaurantCard(restaurant) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';
        
        const card = document.createElement('div');
        card.className = 'restaurant-card';
        
        const ratingStars = '★'.repeat(Math.round(restaurant.dinner_rating)) + 
                           '☆'.repeat(5 - Math.round(restaurant.dinner_rating));

        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${restaurant.name}</h5>
                <p class="card-text">
                    <span class="rating">${ratingStars}</span>
                    <small class="text-muted">(${restaurant.dinner_rating.toFixed(1)})</small>
                </p>
                <p class="card-text">${restaurant.cuisines}</p>
                <p class="card-text"><small class="text-muted">${restaurant.area}</small></p>
                <p class="card-text">₹${restaurant.average_cost} for two</p>
                
                <ul class="features-list">
                    ${restaurant.home_delivery ? '<li><i class="fas fa-motorcycle"></i>Delivery</li>' : ''}
                    ${restaurant.takeaway ? '<li><i class="fas fa-shopping-bag"></i>Takeaway</li>' : ''}
                    ${restaurant.indoor_seating ? '<li><i class="fas fa-chair"></i>Dine-in</li>' : ''}
                </ul>
                
                ${restaurant.popular_dishes ? 
                    `<p class="card-text"><small class="text-muted">Popular: ${restaurant.popular_dishes}</small></p>` : ''}
            </div>
        `;
        
        col.appendChild(card);
        return col;
    }
}); 