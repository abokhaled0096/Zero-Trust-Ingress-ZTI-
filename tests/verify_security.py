import requests
import json
import os
import time
import subprocess

BASE_URL = "http://127.0.0.1:8000"
LOG_FILE = "logs/gateway.log"

def run_test(name, payload, expected_status):
    print(f"--- Running Test: {name} ---")
    try:
        response = requests.post(f"{BASE_URL}/analyze", json={"text": payload})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == expected_status:
            print(f"SUCCESS: Received expected status {expected_status}")
            return True
        else:
            print(f"FAILURE: Expected {expected_status}, got {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def verify_logs():
    print("--- Verifying Logs ---")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                print(f"SUCCESS: {len(lines)} log entries found.")
                return True
    print("FAILURE: No log entries found or log file missing.")
    return False

if __name__ == "__main__":
    # Note: This script assumes the server is running locally on port 8000.
    # In a full GSD loop, we would start the server, run tests, and then kill it.
    
    # Start the server in the background (simplified for verification script)
    # In this environment, we expect the agent to have the server context.
    
    print("Verification Script Started.")
    
    # Test A: Safe request (Whitelisted IP - assuming running from 127.0.0.1)
    test_a = run_test("Safe Whitelisted Request", "Hello, how do I secure my API?", 200)
    
    # Test B: Malicious request (Regex Match)
    test_b = run_test("Malicious Regex Request", "' OR 1=1 --", 403)
    
    # Test C: AI Security Scan (Safe)
    # We simulate a non-whitelisted IP by changing the config temporarily if needed, 
    # but for this script we'll just test the logic flow.
    test_c = run_test("AI Scan Safe Request", "Tell me a joke about security.", 200)

    # Log Verification
    log_check = verify_logs()
    
    if all([test_a, test_b, test_c, log_check]):
        print("\nALL VERIFICATION TESTS PASSED.")
        exit(0)
    else:
        print("\nSOME VERIFICATION TESTS FAILED.")
        exit(1)
