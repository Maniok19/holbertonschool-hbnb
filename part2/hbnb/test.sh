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

# Test creating a user with valid data
test_create_valid_user() {
    print_header "Testing Valid User Creation"
    response=$(curl -s -X POST "$BASE_URL/" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }')
    echo "Response: $response"
    if echo "$response" | grep -q "id"; then
        export USER_ID=$(echo $response | jq -r '.id')
        echo -e "${GREEN}Test passed: User created successfully${NC}"
    else
        echo -e "${RED}Test failed: Could not create user${NC}"
    fi
}

# Test creating a user with invalid email
test_create_invalid_email() {
    print_header "Testing User Creation with Invalid Email"
    response=$(curl -s -X POST "$BASE_URL/" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        }')
    if echo "$response" | grep -q "error"; then
        echo -e "${GREEN}Test passed: Invalid email rejected${NC}"
    else
        echo -e "${RED}Test failed: Invalid email was accepted${NC}"
    fi
}

# Test creating a user with missing fields
test_create_missing_fields() {
    print_header "Testing User Creation with Missing Fields"
    response=$(curl -s -X POST "$BASE_URL/" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "John"
        }')
    if echo "$response" | grep -q "error"; then
        echo -e "${GREEN}Test passed: Missing fields rejected${NC}"
    else
        echo -e "${RED}Test failed: Request with missing fields was accepted${NC}"
    fi
}

# Test creating duplicate user
test_create_duplicate_user() {
    print_header "Testing Duplicate User Creation"
    response=$(curl -s -X POST "$BASE_URL/" \
        -H "Content-Type: application/json" \
        -d '{
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }')
    if echo "$response" | grep -q "Email already registered"; then
        echo -e "${GREEN}Test passed: Duplicate email rejected${NC}"
    else
        echo -e "${RED}Test failed: Duplicate email was accepted${NC}"
    fi
}

# Test getting all users
test_get_users() {
    print_header "Testing Get All Users"
    response=$(curl -s -X GET "$BASE_URL/")
    if [ ! -z "$response" ]; then
        echo -e "${GREEN}Test passed: Retrieved users list${NC}"
        echo "Users: $response"
    else
        echo -e "${RED}Test failed: Could not retrieve users${NC}"
    fi
}

# Test getting user by ID
test_get_user_by_id() {
    print_header "Testing Get User by ID"
    if [ ! -z "$USER_ID" ]; then
        response=$(curl -s -X GET "$BASE_URL/$USER_ID")
        if echo "$response" | grep -q "$USER_ID"; then
            echo -e "${GREEN}Test passed: Retrieved user by ID${NC}"
        else
            echo -e "${RED}Test failed: Could not retrieve user by ID${NC}"
        fi
    else
        echo -e "${RED}No user ID available for testing${NC}"
    fi
}

# Test getting non-existent user
test_get_nonexistent_user() {
    print_header "Testing Get Non-existent User"
    response=$(curl -s -X GET "$BASE_URL/nonexistent-id")
    if echo "$response" | grep -q "not found"; then
        echo -e "${GREEN}Test passed: Non-existent user handling worked${NC}"
    else
        echo -e "${RED}Test failed: Unexpected response for non-existent user${NC}"
    fi
}

# Test updating user with valid data
test_update_user() {
    print_header "Testing Valid User Update"
    if [ ! -z "$USER_ID" ]; then
        response=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
            -H "Content-Type: application/json" \
            -d '{
                "first_name": "Johnny",
                "last_name": "Doe Updated",
                "email": "johnny.updated@example.com"
            }')
        if echo "$response" | grep -q "johnny.updated@example.com"; then
            echo -e "${GREEN}Test passed: User updated successfully${NC}"
        else
            echo -e "${RED}Test failed: User update failed${NC}"
        fi
    else
        echo -e "${RED}No user ID available for testing${NC}"
    fi
}

# Test updating user with invalid data
test_update_invalid_data() {
    print_header "Testing Update with Invalid Data"
    if [ ! -z "$USER_ID" ]; then
        response=$(curl -s -X PUT "$BASE_URL/$USER_ID" \
            -H "Content-Type: application/json" \
            -d '{
                "first_name": "",
                "last_name": "",
                "email": "invalid-email"
            }')
        if echo "$response" | grep -q "error"; then
            echo -e "${GREEN}Test passed: Invalid update data rejected${NC}"
        else
            echo -e "${RED}Test failed: Invalid update data accepted${NC}"
        fi
    else
        echo -e "${RED}No user ID available for testing${NC}"
    fi
}

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
    test_create_valid_user
    test_create_invalid_email
    test_create_missing_fields
    test_create_duplicate_user
    test_get_users
    test_get_user_by_id
    test_get_nonexistent_user
    test_update_user
    test_update_invalid_data
    
    echo -e "\n${GREEN}All tests completed!${NC}"
}

# Run main function
main