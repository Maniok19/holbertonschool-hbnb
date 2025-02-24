#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Base URL for the API
BASE_URL="http://localhost:5000/api/v1/users"

# Function to print section headers
print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}"
}

# Function to check if the API is running
check_api() {
    curl -s "$BASE_URL" > /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: API is not running at $BASE_URL${NC}"
        exit 1
    fi
}

# Test creating a user
test_create_user() {
    print_header "Testing User Creation"
    
    response=$(curl -s -X POST "$BASE_URL/" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }')
    
    echo "Response: $response"
    
    # Use jq to parse JSON and extract ID
    if command -v jq &> /dev/null; then
        export USER_ID=$(echo $response | jq -r '.id')
        if [ "$USER_ID" != "null" ] && [ ! -z "$USER_ID" ]; then
            echo -e "${GREEN}User created successfully with ID: $USER_ID${NC}"
        else
            echo -e "${RED}Failed to create user${NC}"
        fi
    else
        # Fallback if jq is not installed
        export USER_ID=$(echo $response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        if [ ! -z "$USER_ID" ]; then
            echo -e "${GREEN}User created successfully with ID: $USER_ID${NC}"
        else
            echo -e "${RED}Failed to create user${NC}"
        fi
    fi
}

# Test getting a specific user
test_get_user() {
    print_header "Testing Get User by ID"
    
    if [ ! -z "$USER_ID" ]; then
        response=$(curl -s -X GET "$BASE_URL/$USER_ID")
        echo "Response: $response"
    else
        echo -e "${RED}No user ID available for testing${NC}"
    fi
}

# Test updating a user
test_update_user() {
    print_header "Testing Update User"
    
    if [ ! -z "$USER_ID" ]; then
        response=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
            -H "Content-Type: application/json" \
            -d '{
                "first_name": "Johnny",
                "last_name": "Doe",
                "email": "johnny.doe@example.com"
            }')
        echo "Response: $response"
    else
        echo -e "${RED}No user ID available for testing${NC}"
    fi
}

# Rest of the functions remain the same...

# Main execution
main() {
    echo -e "${BLUE}Starting API Tests${NC}"
    
    # Install jq if not present
    if ! command -v jq &> /dev/null; then
        echo "Installing jq for JSON parsing..."
        sudo apt-get update && sudo apt-get install -y jq
    fi
    
    # Check if API is running
    check_api
    
    # Run all tests
    test_create_user
    test_duplicate_user
    test_get_users
    test_get_user
    test_update_user
    
    echo -e "\n${GREEN}All tests completed!${NC}"
}

# Run main function
main