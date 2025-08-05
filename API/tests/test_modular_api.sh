#!/bin/bash

# Test script for Modular Pipeline API
# This script tests all endpoints of the modular pipeline API

API_BASE_URL="http://localhost:8001"
TEST_YOUTUBE_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================================"
echo -e "${BLUE}🧪 Testing Modular Pipeline API${NC}"
echo "============================================================"

# Function to test API endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "${YELLOW}Testing: ${description}${NC}"
    echo "Endpoint: ${method} ${API_BASE_URL}${endpoint}"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "${API_BASE_URL}${endpoint}")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "${API_BASE_URL}${endpoint}")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}✅ SUCCESS (HTTP $http_code)${NC}"
        echo "Response: $(echo "$body" | jq -r '.message // .status // "OK"' 2>/dev/null || echo "$body" | head -c 100)"
    else
        echo -e "${RED}❌ FAILED (HTTP $http_code)${NC}"
        echo "Response: $body"
    fi
    echo "---"
}

# Check if API is running
echo -e "${BLUE}🔍 Checking if API is running...${NC}"
if ! curl -s "${API_BASE_URL}/health" > /dev/null; then
    echo -e "${RED}❌ API is not running at ${API_BASE_URL}${NC}"
    echo "Please start the modular pipeline API first:"
    echo "cd API && python3 modular_pipeline.py"
    exit 1
fi
echo -e "${GREEN}✅ API is running${NC}"
echo ""

# Test GET endpoints
test_endpoint "GET" "/" "" "Root endpoint - API information"
test_endpoint "GET" "/health" "" "Health check"
test_endpoint "GET" "/status" "" "Status check"

# Test pipeline endpoints with YouTube URL
echo -e "${BLUE}🎬 Testing YouTube-dependent endpoints${NC}"
test_endpoint "POST" "/validate-youtube-url" "{\"youtube_url\": \"$TEST_YOUTUBE_URL\"}" "Validate YouTube URL"
test_endpoint "POST" "/download-video" "{\"youtube_url\": \"$TEST_YOUTUBE_URL\"}" "Download Video (WARNING: This will actually download!)"
test_endpoint "POST" "/extract-audio-transcript" "{\"youtube_url\": \"$TEST_YOUTUBE_URL\"}" "Extract Audio Transcript"

# Test pipeline endpoints without YouTube URL (these may fail if previous steps haven't run)
echo -e "${BLUE}🔄 Testing pipeline-dependent endpoints${NC}"
echo -e "${YELLOW}Note: These may fail if the pipeline hasn't been run sequentially${NC}"
test_endpoint "POST" "/extract-video-frames" "{}" "Extract Video Frames"
test_endpoint "POST" "/deduplicate-frames" "{}" "Deduplicate Frames"
test_endpoint "POST" "/generate-visual-descriptions" "{}" "Generate Visual Descriptions"
test_endpoint "POST" "/merge-audio-visual" "{}" "Merge Audio Visual"
test_endpoint "POST" "/extract-visual-objects" "{}" "Extract Visual Objects"
test_endpoint "POST" "/enrich-with-figure-tags" "{}" "Enrich with Figure Tags"
test_endpoint "POST" "/generate-ascii-art" "{}" "Generate ASCII Art"
test_endpoint "POST" "/generate-braille-art" "{}" "Generate Braille Art"
test_endpoint "POST" "/assemble-final-document" "{}" "Assemble Final Document"
test_endpoint "POST" "/finalize-output" "{}" "Finalize Output"

echo "============================================================"
echo -e "${BLUE}🏁 Testing Complete${NC}"
echo "============================================================"
echo ""
echo -e "${YELLOW}📝 Notes:${NC}"
echo "1. Some endpoints may fail if dependencies from previous steps are missing"
echo "2. To run a full pipeline test, execute the steps sequentially"
echo "3. Check the API logs for detailed error information"
echo "4. The download-video test actually downloads a video - use with caution"
echo ""
echo -e "${BLUE}🔗 Useful URLs:${NC}"
echo "• API Documentation: ${API_BASE_URL}/docs"
echo "• API Root Info: ${API_BASE_URL}/"
echo "• Health Check: ${API_BASE_URL}/health"
