# app/config/env_config.py
import os
import random
from typing import List

from dotenv import load_dotenv

from app.core.configs.base_config import BaseConfig

class EnvSettings:
    user_agents: List[str] = [
        "EventLocationService/1.0 (dummy121@example.com)",
        "EventLocationService/1.0 (dummy2324@example.com)",
        "EventLocationService/1.0 (dummy342343@example.com)",
        "EventLocationService/1.0 (dummy4342@example.com)",
        "EventLocationService/1.0 (dummy324235@example.com)",
        "EventLocationService/1.0 (dummy63242@example.com)",
        "EventLocationService/1.0 (dummy72343@example.com)",
        "EventLocationService/1.0 (dummy83432@example.com)",
        "EventLocationService/1.0 (dummy9342@example.com)",
        "EventLocationService/1.0 (dummy13240@example.com)",
    ]

class EnvConfig(BaseConfig):
    def __init__(self):
        load_dotenv() 
        self.settings = EnvSettings()

    def get_user_agents(self) -> List[str]:
        return self.settings.user_agents

    def get_random_user_agent(self) -> str:
        return random.choice(self.settings.user_agents)
    
    def get_api_key(self) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("LLM_API_KEY environment variable is not set")
        return api_key