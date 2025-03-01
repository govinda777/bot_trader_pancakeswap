import os
import sys
import pytest
from dotenv import load_dotenv
from src.environment import ENV_SETTINGS

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def env_settings():
    return ENV_SETTINGS