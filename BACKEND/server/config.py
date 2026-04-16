from datetime import timedelta
from dotenv import load_dotenv
import os
from urllib.parse import urlsplit, urlunsplit

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')
load_dotenv(ENV_PATH, override=True)
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)


def _running_in_docker():
    return os.path.exists('/.dockerenv')


def _swap_db_host_to_localhost(db_url: str) -> str:
    """When running outside Docker, replace docker hostname `db` with localhost."""
    try:
        parsed = urlsplit(db_url)
        if parsed.hostname != 'db':
            return db_url

        username = parsed.username or ''
        password = parsed.password or ''
        auth = username
        if password:
            auth = f"{auth}:{password}"
        if auth:
            auth = f"{auth}@"

        host = 'localhost'
        port = parsed.port or 5432
        netloc = f"{auth}{host}:{port}"
        return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))
    except Exception:
        return db_url

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # If DATABASE_URL is not provided, default to the seeded SQLite file in instance dir
    _default_sqlite_path = os.path.join(INSTANCE_DIR, 'portfolio.db')
    _default_sqlite_uri = f"sqlite:///{_default_sqlite_path}"
    _database_url = os.getenv('DATABASE_URL', _default_sqlite_uri)
    _local_database_url = os.getenv('LOCAL_DATABASE_URL')

    if not _running_in_docker():
        if _local_database_url:
            _database_url = _local_database_url
        else:
            _database_url = _swap_db_host_to_localhost(_database_url)

    SQLALCHEMY_DATABASE_URI = _database_url

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