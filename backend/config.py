import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

DATABASE_URL = CONFIG["database"]["url"]
SECRET_KEY = CONFIG["auth"]["secret_key"]
ALGORITHM = CONFIG["auth"]["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = CONFIG["auth"]["access_token_expire_minutes"]
CORS_ORIGINS = CONFIG["cors"]["allow_origins"]
