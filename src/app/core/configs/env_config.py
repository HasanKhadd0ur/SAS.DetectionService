# app/config/env_config.py
import os
import random
from typing import Dict, List

from dotenv import load_dotenv
from pymongo import MongoClient

from app.core.configs.base_config import BaseConfig
uri = "mongodb://localhost:27017"
mongo_db_name = "detection"
config_collection_name = "config"

class EnvSettings:
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client[mongo_db_name]
        self.config_collection = self.db[config_collection_name]

        self._configs_cache: Dict[str, dict] = {}

        # Load user agents from DB, fallback to empty list if not found
        try:
            self.user_agents: List[str] = self.get_config_from_db("USER_AGENTS")
        except KeyError:
            self.user_agents = []
            print("Warning: No USER_AGENTS config found in DB, using empty list.")

    def get_config_from_db(self, key: str) -> dict:
        if key in self._configs_cache:
            return self._configs_cache[key]
        
        result = self.config_collection.find_one({"key": key})
        if not result or "config" not in result:
            raise KeyError(f"No config found in DB for key: {key}")
                
        self._configs_cache[key] = result["config"]
        return result["config"]

    def get_pipeline_config(self) -> dict:
        return self.get_config_from_db("DETECTION_PIPELINE_CONFIG")    

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
    
    def get_topic_keywords(self, topic: str) -> List[str]:
        try:
            keyword_map = self.settings.get_config_from_db("TOPIC_KEYWORDS")
            return keyword_map.get(topic, [])
        except KeyError:
            print("Warning: TOPIC_KEYWORDS config not found in DB.")
            return []