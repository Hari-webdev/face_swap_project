"""Application Settings"""
import os
from dotenv import load_dotenv

load_dotenv()

# Replicate API Token
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# Model Configuration
FACE_SWAP_MODEL = os.getenv(
    "FACE_SWAP_MODEL",
    "cdingram/face-swap:d1d6ea8c8be89d664a07a457526f7128109dee7030fdac424788d762c71ed111",
)

# Directories
RESULT_DIR = os.getenv("RESULT_DIR", "app/static/results")

# Timeouts
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))

# Optional: Imgbb upload
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")
IMGBB_EXPIRATION = int(os.getenv("IMGBB_EXPIRATION", "600"))
