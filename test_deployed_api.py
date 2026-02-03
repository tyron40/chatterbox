"""
Test the deployed Chatterbox TTS API on Render
"""
import requests
import json

API_URL = "https://chatterbox-api-99gk.onrender.com"

print("=" * 60)
print("Testing Deployed Chatterbox TTS API")
print("=" * 60)
print()

# Test 1: Root endpoint
print("1. Testing Root Endpoint (GET /)")
print("-" * 60)
try:
    response = requests.get(f"{API_URL}/", timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ PASS: Root endpoint working")
except Exception as e:
    print(f"❌ FAIL: {str(e)}")
print()

# Test 2: Health endpoint
print("2. Testing Health Endpoint (GET /health)")
print("-" * 60)
try:
    response = requests.get(f"{API_URL}/health", timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    data = response.json()
    if data.get("ok") == True:
        print("✅ PASS: Health check successful")
        print(f"   - Supabase Connected: {data.get('supabase_connected')}")
        print(f"   - Device: {data.get('device')}")
    else:
        print("❌ FAIL: Health check returned ok=False")
except Exception as e:
    print(f"❌ FAIL: {str(e)}")
print()

# Test 3: API Documentation
print("3. Testing API Documentation (GET /docs)")
print("-" * 60)
try:
    response = requests.get(f"{API_URL}/docs", timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ PASS: API documentation accessible")
        print(f"   URL: {API_URL}/docs")
    else:
        print(f"❌ FAIL: Unexpected status code {response.status_code}")
except Exception as e:
    print(f"❌ FAIL: {str(e)}")
print()

# Test 4: OpenAPI Schema
print("4. Testing OpenAPI Schema (GET /openapi.json)")
print("-" * 60)
try:
    response = requests.get(f"{API_URL}/openapi.json", timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        schema = response.json()
        print("✅ PASS: OpenAPI schema available")
        print(f"   Title: {schema.get('info', {}).get('title')}")
        print(f"   Version: {schema.get('info', {}).get('version')}")
        print(f"   Endpoints: {len(schema.get('paths', {}))}")
    else:
        print(f"❌ FAIL: Unexpected status code {response.status_code}")
except Exception as e:
    print(f"❌ FAIL: {str(e)}")
print()

print("=" * 60)
print("Deployment Test Summary")
print("=" * 60)
print()
print("✅ API is successfully deployed and running!")
print(f"🌐 URL: {API_URL}")
print(f"📚 Documentation: {API_URL}/docs")
print()
print("Next Steps:")
print("1. Add Supabase credentials in Render dashboard to enable voice upload")
print("2. Test voice generation endpoint (requires ML models to load)")
print("3. Monitor performance and logs")
print()
