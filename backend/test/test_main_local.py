"""Backend tests for the FastAPI backend using in-memory task list for storage"""

from backend import settings

settings.BACKEND_MODE = "local"
from backend.test.main_template import *
