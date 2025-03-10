# HBnB API

This project is an API for the HBnB application, developed as an exercise for Holberton School. The API provides endpoints for managing users, places, amenities, and reviews.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
    - [Users](#users)
    - [Places](#places)
    - [Amenities](#amenities)
    - [Reviews](#reviews)
- [Models](#models)
- [Services](#services)
- [Configuration](#configuration)
- [Testing](#testing)
- [License](#license)

## Installation

1. Clone the repository:
        ```bash
        git clone https://github.com/yourusername/holbertonschool-hbnb.git
        cd holbertonschool-hbnb/part2/hbnb
        ```


2. Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```

## Usage

1. Run the application:
        ```bash
        python3 run.py
        ```

2. The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Users

- **GET /api/v1/users/**: Retrieve a list of all users.
- **POST /api/v1/users/**: Create a new user.
- **GET /api/v1/users/<user_id>**: Retrieve a user by ID.
- **PUT /api/v1/users/<user_id>**: Update a user by ID.

### Places

- **GET /api/v1/places/**: Retrieve a list of all places.
- **POST /api/v1/places/**: Create a new place.
- **GET /api/v1/places/<place_id>**: Retrieve a place by ID.
- **PUT /api/v1/places/<place_id>**: Update a place by ID.
- **GET /api/v1/places/<place_id>/reviews**: Retrieve all reviews for a specific place.

### Amenities

- **GET /api/v1/amenities/**: Retrieve a list of all amenities.
- **POST /api/v1/amenities/**: Create a new amenity.
- **GET /api/v1/amenities/<amenity_id>**: Retrieve an amenity by ID.
- **PUT /api/v1/amenities/<amenity_id>**: Update an amenity by ID.

### Reviews

- **GET /api/v1/reviews/**: Retrieve a list of all reviews.
- **POST /api/v1/reviews/**: Create a new review.
- **GET /api/v1/reviews/<review_id>**: Retrieve a review by ID.
- **PUT /api/v1/reviews/<review_id>**: Update a review by ID.
- **DELETE /api/v1/reviews/<review_id>**: Delete a review by ID.
- **GET /api/v1/places/<place_id>/reviews**: Retrieve all reviews for a specific place.

## Models

- **User**: Represents a user in the system.
- **Place**: Represents a place in the system.
- **Amenity**: Represents an amenity in the system.
- **Review**: Represents a review in the system.

## Services

The services layer handles the business logic and interactions with the data repository.

## Configuration

Configuration settings are managed in `config.py`. The default configuration is for development.

## Testing

To run the tests, use the following command:
```bash
python3 tests.py
```

# Authors
Esteban Cratere


Mano Delcourt 


Herve Le Guennec