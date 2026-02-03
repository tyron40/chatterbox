"""
Check Render deployment status using Render API
"""
import requests
import os
import time
from datetime import datetime

# You'll need to set your Render API key as an environment variable
# Get it from: https://dashboard.render.com/u/settings#api-keys
RENDER_API_KEY = os.getenv("RENDER_API_KEY", "")

if not RENDER_API_KEY:
    print("⚠️  RENDER_API_KEY environment variable not set")
    print("📝 To use this script:")
    print("   1. Go to https://dashboard.render.com/u/settings#api-keys")
    print("   2. Create an API key")
    print("   3. Set it: $env:RENDER_API_KEY='your-key-here'")
    print("   4. Run this script again")
    exit(1)

HEADERS = {
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Accept": "application/json"
}

BASE_URL = "https://api.render.com/v1"

def get_services():
    """Get all services"""
    response = requests.get(f"{BASE_URL}/services", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error getting services: {response.status_code}")
        print(response.text)
        return None

def get_service_details(service_id):
    """Get details for a specific service"""
    response = requests.get(f"{BASE_URL}/services/{service_id}", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error getting service details: {response.status_code}")
        return None

def get_deploys(service_id, limit=5):
    """Get recent deploys for a service"""
    response = requests.get(
        f"{BASE_URL}/services/{service_id}/deploys",
        headers=HEADERS,
        params={"limit": limit}
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error getting deploys: {response.status_code}")
        return None

def get_deploy_logs(service_id, deploy_id):
    """Get logs for a specific deploy"""
    response = requests.get(
        f"{BASE_URL}/services/{service_id}/deploys/{deploy_id}/logs",
        headers=HEADERS
    )
    if response.status_code == 200:
        return response.text
    else:
        print(f"❌ Error getting logs: {response.status_code}")
        return None

def main():
    print("🔍 Fetching Render services...")
    services_data = get_services()
    
    if not services_data:
        return
    
    services = services_data.get("services", [])
    
    if not services:
        print("❌ No services found")
        return
    
    print(f"\n📦 Found {len(services)} service(s):\n")
    
    for idx, service in enumerate(services, 1):
        name = service.get("name", "Unknown")
        service_id = service.get("id", "")
        service_type = service.get("type", "")
        
        print(f"{idx}. {name}")
        print(f"   ID: {service_id}")
        print(f"   Type: {service_type}")
        
        # Get service details
        details = get_service_details(service_id)
        if details:
            service_url = details.get("serviceDetails", {}).get("url", "N/A")
            print(f"   URL: {service_url}")
        
        # Get recent deploys
        deploys_data = get_deploys(service_id, limit=3)
        if deploys_data:
            deploys = deploys_data.get("deploys", [])
            if deploys:
                print(f"\n   📋 Recent Deploys:")
                for deploy in deploys[:3]:
                    deploy_id = deploy.get("id", "")
                    status = deploy.get("status", "unknown")
                    created_at = deploy.get("createdAt", "")
                    commit_id = deploy.get("commit", {}).get("id", "N/A")[:7]
                    commit_msg = deploy.get("commit", {}).get("message", "N/A")
                    
                    status_emoji = {
                        "live": "✅",
                        "build_in_progress": "🔄",
                        "update_in_progress": "🔄",
                        "build_failed": "❌",
                        "update_failed": "❌",
                        "canceled": "⚠️"
                    }.get(status, "❓")
                    
                    print(f"   {status_emoji} {status.upper()}")
                    print(f"      Commit: {commit_id} - {commit_msg[:50]}")
                    print(f"      Created: {created_at}")
                    
                    # If this is the latest deploy and it's in progress, show logs
                    if deploy == deploys[0] and "in_progress" in status:
                        print(f"\n   📜 Latest Deploy Logs:")
                        logs = get_deploy_logs(service_id, deploy_id)
                        if logs:
                            # Show last 20 lines
                            log_lines = logs.strip().split('\n')
                            for line in log_lines[-20:]:
                                print(f"      {line}")
                    print()
        
        print("-" * 60)
        print()

if __name__ == "__main__":
    main()
