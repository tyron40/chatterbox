"""Test Supabase connection"""
import os
from supabase import create_client

# Set environment variables
os.environ["SUPABASE_URL"] = "https://iwitmebruaqivzkacecs.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3aXRtZWJydWFxaXZ6a2FjZWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODM1NTU0NiwiZXhwIjoyMDUzOTMxNTQ2fQ.QL_3_PqJEKNLKdxOCKhH-jPqYVJqxWLWYqPPqYVJqxU"
os.environ["SUPABASE_BUCKET"] = "voices"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "voices")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_BUCKET: {SUPABASE_BUCKET}")
print(f"SUPABASE_SERVICE_ROLE_KEY: {SUPABASE_SERVICE_ROLE_KEY[:20]}...")

try:
    print("\nCreating Supabase client...")
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    print(f"✅ Supabase client created: {supabase is not None}")
    
    print("\nTesting storage access...")
    result = supabase.storage.from_(SUPABASE_BUCKET).list()
    print(f"✅ Storage accessible! Found {len(result)} files")
    
    for item in result:
        print(f"  - {item.get('name')}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
