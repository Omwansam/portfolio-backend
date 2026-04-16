from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # If DATABASE_URL is not provided, default to the seeded SQLite file in instance dir
    _default_sqlite_path = os.path.join(INSTANCE_DIR, 'portfolio.db')
    _default_sqlite_uri = f"sqlite:///{_default_sqlite_path}"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', _default_sqlite_uri)

    # For SQLite under Gunicorn, ensure thread safety and connectivity
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite:///') and 'check_same_thread' not in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI += '?check_same_thread=false'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    _cors_origins = os.getenv('CORS_ORIGINS', '*')
    CORS_ORIGINS = [origin.strip() for origin in _cors_origins.split(',') if origin.strip()]

    #File Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')  # Local storage
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Mail settings (loaded from .env)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'false' and False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # For Gmail, the sender email should be the authenticated account (MAIL_USERNAME)
    _mail_username = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = (
        os.getenv('MAIL_DEFAULT_NAME', 'My Website'),
        _mail_username or os.getenv('MAIL_DEFAULT_EMAIL', 'noreply@example.com')
    )