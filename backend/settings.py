from dotenv import dotenv_values
from typing import Literal
import os

IS_PROD: bool = False
MONGODB_URI: str = ""
BACKEND_MODE: Literal["db"] | Literal["local"] = "local"


def _get_config(key: str, vals: dict, env_file: str) -> str:
    val = vals.get(key)
    if val is None or val == "":
        raise ValueError(f"No environment variable found for {key} in {env_file}")
    return val


def _make_config():
    global IS_PROD, MONGODB_URI, BACKEND_MODE
    IS_PROD = os.getenv("TODO_PRODUCTION") is not None
    env_file = ".env.prod" if IS_PROD else ".env.dev"
    env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), env_file)
    vals = dotenv_values(env_file)
    MONGODB_URI = _get_config("MONGODB_URI", vals, env_file)
    be_mode = _get_config("BACKEND_MODE", vals, env_file)
    if be_mode != "db" and be_mode != "local":
        raise ValueError(f'BACKEND_MODE must be one of "db" | "local"')
    BACKEND_MODE = be_mode


_make_config()
