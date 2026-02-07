import requests
import json

class APITestTemplate:
    def __init__(self, base_url, auth_token=None):
        self.base_url = base_url.rstrip('/')
        self.headers = {"Content-Type": "application/json"}
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    def set_auth_token(self, token):
        self.headers["Authorization"] = f"Bearer {token}"

    def log(self, message):
        print(f"[TEST LOG] {message}")

    def test_endpoint(self, method, endpoint, expected_status=200, payload=None, description=""):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.log(f"Testing {description} -> {method} {url}")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=payload)
            else:
                self.log(f"Unsupported method: {method}")
                return None

            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code == expected_status:
                self.log("✅ PASSED")
            else:
                self.log(f"❌ FAILED. Expected {expected_status}, got {response.status_code}")
            
            return response
        except Exception as e:
            self.log(f"❌ EXCEPTION: {e}")
            return None

if __name__ == "__main__":
    # Example Usage
    api_url = "http://localhost:8000"
    # Replace with a valid Clerk Token for actual testing
    test_token = "YOUR_CLERK_TOKEN_HERE" 
    
    tester = APITestTemplate(api_url, test_token)
    
    # 1. Test Public Endpoint
    tester.test_endpoint("GET", "/public", 200, description="Public Endpoint")

    # 2. Test Protected Endpoint (Credits check)
    # tester.test_endpoint("GET", "/protected", 200, description="Protected Info")

    # 3. Test Credit Consumption
    # tester.test_endpoint("POST", "/generate-ai", 200, description="AI Generation (5 credits)")

    # 4. Test Refund Logic
    # tester.test_endpoint("POST", "/failing-endpoint", 400, description="Failing Endpoint (Refund)")
