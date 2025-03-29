import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:minsi@localhost/sdgp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Supabase configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://qcjvyvipblxqjqlfmict.supabase.co')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjanZ5dmlwYmx4cWpxbGZtaWN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEzMzc4NDAsImV4cCI6MjA1NjkxMzg0MH0.4hmGPxAONFwokBqhMVI_vuZQzD_WkiYpmtbT0V3uHps')