
import sys
import pytest
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from environment import EnvironmentSettings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.fixture(scope="session")
def env_settings():
    return EnvironmentSettings()