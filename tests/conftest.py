
import pytest
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from environment import EnvironmentSettings

@pytest.fixture(scope="session")
def env_settings():
    return EnvironmentSettings()