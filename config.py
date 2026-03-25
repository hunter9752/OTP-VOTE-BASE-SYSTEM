# Configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
    
    # Supabase PostgreSQL connection
    # Note: @ symbol in password must be URL-encoded as %40
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:Siddhi%4097sk@db.uyrlykevxyqimthntpxv.supabase.co:5432/postgres')
    
    # OTP settings
    OTP_EXPIRY_MINUTES = 5
    
    # Email settings (for OTP delivery)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', 'noreply@voting.com')
    
    # Testing mode (prints OTP to console instead of sending email)
    TESTING_MODE = os.getenv('TESTING_MODE', 'True').lower() == 'true'
