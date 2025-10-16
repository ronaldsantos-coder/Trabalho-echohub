import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://txfevmlhzqchiylfewrz.supabase.co')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4ZmV2bWxoenFjaGl5bGZld3J6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxNTM5NDksImV4cCI6MjA3NDcyOTk0OX0.Fjz4_RkeZMWXTdeAsHVmEHY6schtADJ1ijlu5FYxJLI')

# Configurações do banco local (fallback)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'password')
DB_NAME = os.getenv('DB_NAME', 'blog_db')
