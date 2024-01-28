""" Setting API file for FASTAPI project."""
import os
from dotenv import load_dotenv

# Load environment variables with dotenv
# if you want to use .env file
load_dotenv()

# Set environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ.get("ACCESS_TOKEN_EXPIRE_SECONDS"))
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_SECONDS"))
