from abc import ABC, abstractmethod
from typing import List

class BaseConfig(ABC):
    @abstractmethod
    def get_user_agents(self) -> List[str]:
        pass

    @abstractmethod
    def get_random_user_agent(self) -> str:
        pass
    def get_api_key(self)->str:
        pass
    
    @abstractmethod
    def get_topic_keywords(self, topic: str) -> List[str]:
        """Return a list of keywords for a given topic name"""
        pass