#!/bin/bash

# Base API URL
BASE_URL="http://localhost:8000/api/v1/conferences"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Starting Conference API tests..."

# Test 1: Create conference
echo -e "\n${GREEN}Test 1: Create conference${NC}"
CREATE_RESPONSE=$(curl -s -X POST "${BASE_URL}/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "conf-001",
    "title": "Python Web Development Workshop",
    "description": "Learn about modern Python web development",
    "start_time": "2024-03-20T10:00:00Z",
    "end_time": "2024-03-20T18:00:00Z",
    "status": "scheduled",
    "meeting_link": "https://zoom.us/j/123456789",
    "organizer_email": "organizer@example.com",
    "max_participants": 100,
    "registration_deadline": "2024-03-19T23:59:59Z",
    "timezone": "UTC",
    "tags": ["python", "web", "workshop"]
  }')
echo "Response: $CREATE_RESPONSE"

# Test 2: Get created conference
echo -e "\n${GREEN}Test 2: Get conference${NC}"
GET_RESPONSE=$(curl -s -X GET "${BASE_URL}/conf-001")
echo "Response: $GET_RESPONSE"

# Test 3: Update conference
echo -e "\n${GREEN}Test 3: Update conference${NC}"
UPDATE_RESPONSE=$(curl -s -X PUT "${BASE_URL}/conf-001" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "conf-001",
    "title": "Advanced Python Web Development Workshop",
    "description": "Deep dive into modern Python web development",
    "start_time": "2024-03-21T10:00:00Z",
    "end_time": "2024-03-21T18:00:00Z",
    "status": "scheduled",
    "meeting_link": "https://zoom.us/j/987654321",
    "organizer_email": "organizer@example.com",
    "max_participants": 150,
    "registration_deadline": "2024-03-20T23:59:59Z",
    "timezone": "UTC",
    "tags": ["python", "web", "advanced", "workshop"]
  }')
echo "Response: $UPDATE_RESPONSE"

# Test 4: Get all conferences
echo -e "\n${GREEN}Test 4: List all conferences${NC}"
LIST_RESPONSE=$(curl -s -X GET "${BASE_URL}/")
echo "Response: $LIST_RESPONSE"

# Test 5: Try to get non-existent conference
echo -e "\n${GREEN}Test 5: Get non-existent conference${NC}"
NOT_FOUND_RESPONSE=$(curl -s -X GET "${BASE_URL}/non-existent-id")
echo "Response: $NOT_FOUND_RESPONSE"

# Test 6: Delete conference
echo -e "\n${GREEN}Test 6: Delete conference${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "${BASE_URL}/conf-001")
echo "Response: $DELETE_RESPONSE"

# Test 7: Verify deletion (try to get deleted conference)
echo -e "\n${GREEN}Test 7: Verify deletion${NC}"
GET_DELETED_RESPONSE=$(curl -s -X GET "${BASE_URL}/conf-001")
echo "Response: $GET_DELETED_RESPONSE"

echo -e "\n${GREEN}Testing completed${NC}" 