from supabase import create_client
import os

# 🔑 Tes identifiants Supabase (tu peux les mettre dans .env plus tard)
SUPABASE_URL = "https://ahyacvlecgpqfylighcn.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoeWFjdmxlY2dwcWZ5bGlnaGNuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQzNTA3NjYsImV4cCI6MjA3OTkyNjc2Nn0.e3fMgFhnr2cLxAW4wlx-6EJpra6OXB6stTKx_H5ioBg"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
