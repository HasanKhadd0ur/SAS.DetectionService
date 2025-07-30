import requests
import re
from collections import defaultdict
from typing import List
from app.core.configs.base_config import BaseConfig


class TopicClassificationService:
    DEFAULT_TOPIC = "أخبار سياسية عامة"
    TOPICS_API_URL =''
    
    def __init__(self, config: BaseConfig,api_url="http://localhost:5200"):
        self.config = config
        self.topics: List[str] = []
        self.TOPICS_API_URL= api_url + '/api/topics'
        self._initialized = False

    def _initialize_topics(self):
        """Fetch topic names from EventService and store them."""
        if self._initialized:
            return

        try:
            response = requests.get(self.TOPICS_API_URL)
            response.raise_for_status()
            data = response.json()
            self.topics = [topic["name"] for topic in data]
            self._initialized = True
        except Exception as e:
            print(f"Failed to fetch topics: {e}")
            self._initialized = True  # Prevent retry loop

    def predict_topic(self, summary: str) -> str:
        """Predict topic based on summary content."""
        self._initialize_topics()
        summary_words = set(self._normalize_text(summary).split())
        match_counts = defaultdict(int)

        for topic in self.topics:
            keywords = self.config.get_topic_keywords(topic)
            for keyword in keywords:
                if keyword in summary_words:
                    match_counts[topic] += 1

        if not match_counts:
            return self.DEFAULT_TOPIC

        return max(match_counts.items(), key=lambda x: x[1])[0]

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"[^\w\s]", "", text).strip()
