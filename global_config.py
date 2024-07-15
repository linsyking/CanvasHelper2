from passlib.context import CryptContext

user_conf_path = "./canvas/user_configs/"
user_cache_path = "./canvas/user_caches/"

DATABASE = "canvas/canvas.db"

uvicorn_domain = "localhost"  # Used to start uvicorn locally by running: `python canvas_app.py`
uvicorn_port = 9283

# Private key name: key.pem
# Public key name: cert.pem

NUM_OF_THREADS = 1  # 1 for running locally, (2*cores+1) for running on server

RELOAD = False  # True for development

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 1 day
REFRESH_TOKEN_EXPIRE_DAYS = 30  # 30 days

ALLOWED_EXTENSION = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "mp4",
    "mkv",
    "mov",
    "m4v",
    "avi",
    "wmv",
    "webm",
}  # svg removed to prevent XSS
