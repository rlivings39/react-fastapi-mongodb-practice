"""Backend tests for the FastAPI backend using MongoDB for storage"""

from backend import settings

settings.BACKEND_MODE = "db"
from backend.test.main_template import *
