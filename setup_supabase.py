"""
Supabase Storage Setup Script
Automatically creates and configures the storage bucket for Chatterbox TTS
"""
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://iwitmebruaqivzkacecs.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3aXRtZWJydWFxaXZ6a2FjZWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTk4MjI2OSwiZXhwIjoyMDg1NTU4MjY5fQ.H_gb3dj7Lz46LhbYY3pc7nBQLOkiyt4yjOj0-58NyCA"
BUCKET_NAME = "voices"

def setup_storage():
    """Set up Supabase storage bucket for voice files"""
    print("🚀 Starting Supabase Storage Setup...")
    print(f"📡 Connecting to: {SUPABASE_URL}")
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Connected to Supabase successfully!")
        
        # Check if bucket exists
        print(f"\n📦 Checking if bucket '{BUCKET_NAME}' exists...")
        try:
            buckets = supabase.storage.list_buckets()
            bucket_exists = any(bucket['name'] == BUCKET_NAME for bucket in buckets)
            
            if bucket_exists:
                print(f"✅ Bucket '{BUCKET_NAME}' already exists!")
            else:
                print(f"📦 Creating bucket '{BUCKET_NAME}'...")
                # Create public bucket
                supabase.storage.create_bucket(
                    BUCKET_NAME,
                    options={"public": True}
                )
                print(f"✅ Bucket '{BUCKET_NAME}' created successfully!")
        
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"✅ Bucket '{BUCKET_NAME}' already exists!")
            else:
                print(f"❌ Error with bucket: {e}")
                print("⚠️  You may need to create the bucket manually in Supabase dashboard")
        
        # Test upload
        print("\n🧪 Testing file upload...")
        test_content = b"Test voice file"
        test_filename = "test_voice.txt"
        
        try:
            # Upload test file
            supabase.storage.from_(BUCKET_NAME).upload(
                test_filename,
                test_content,
                file_options={"content-type": "text/plain"}
            )
            print(f"✅ Test file uploaded successfully!")
            
            # Get public URL
            public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(test_filename)
            print(f"📎 Public URL: {public_url}")
            
            # Clean up test file
            supabase.storage.from_(BUCKET_NAME).remove([test_filename])
            print(f"🧹 Test file cleaned up")
            
        except Exception as e:
            if "already exists" in str(e).lower():
                print("⚠️  Test file already exists, cleaning up...")
                supabase.storage.from_(BUCKET_NAME).remove([test_filename])
                print("✅ Cleanup successful")
            else:
                print(f"❌ Upload test failed: {e}")
                print("⚠️  Check bucket permissions in Supabase dashboard")
        
        print("\n" + "="*50)
        print("✅ Supabase Storage Setup Complete!")
        print("="*50)
        print(f"\n📋 Configuration Summary:")
        print(f"   Supabase URL: {SUPABASE_URL}")
        print(f"   Bucket Name: {BUCKET_NAME}")
        print(f"   Bucket Status: Public")
        print(f"\n🎯 Next Steps:")
        print(f"   1. Go to Render dashboard")
        print(f"   2. Add environment variables:")
        print(f"      - SUPABASE_URL: {SUPABASE_URL}")
        print(f"      - SUPABASE_SERVICE_ROLE_KEY: {SUPABASE_KEY}")
        print(f"      - SUPABASE_BUCKET: {BUCKET_NAME}")
        print(f"   3. Deploy your service")
        print(f"\n🌐 Your API will be ready at: https://your-app.onrender.com")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your Supabase credentials")
        print("   2. Ensure your project is active")
        print("   3. Verify network connection")
        return False
    
    return True

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   Chatterbox TTS - Supabase Storage Setup       ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    success = setup_storage()
    
    if success:
        print("\n✨ Setup completed successfully!")
    else:
        print("\n⚠️  Setup encountered errors. Please check the output above.")
