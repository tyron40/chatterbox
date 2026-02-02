@echo off
echo Setting up Supabase environment variables...
set SUPABASE_URL=https://iwitmebruaqivzkacecs.supabase.co
set SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml3aXRtZWJydWFxaXZ6a2FjZWNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODM1NTU0NiwiZXhwIjoyMDUzOTMxNTQ2fQ.QL_3_PqJEKNLKdxOCKhH-jPqYVJqxWLWYqPPqYVJqxU
set SUPABASE_BUCKET=voices

echo.
echo Environment variables set!
echo SUPABASE_URL=%SUPABASE_URL%
echo SUPABASE_BUCKET=%SUPABASE_BUCKET%
echo.
echo Starting API server with Supabase configured...
uvicorn api:app --reload --host 0.0.0.0 --port 8000
