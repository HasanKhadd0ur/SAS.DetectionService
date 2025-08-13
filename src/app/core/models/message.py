from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import numpy as np

@dataclass
class Message:
    id:str=""
    source: str=""
    domain: str=""
    platform: str=""
    domainId: str=""
    raw_content: str=""
    content: str=""
    sentiment_label: str=""
    sentiment_score: float =0
    platform_id:str="1e9cfd36-e1e8-49dc-abe7-d8e983ec2dd3"
    created_at: datetime = datetime.utcnow()
    embedding: Optional[List[float]] = None
    
    metadata: dict = None
    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def serialize_message(self) -> dict:
        
        return {
            "messageId": self.id,
            "content": self.content,
            "source": self.source,
            "platform": self.platform,
            "platformId": self.platform_id,
            "createdAt": self.created_at.isoformat(),
            "sentimentLabel": self.sentiment_label,
            "sentimentScore": str(self.sentiment_score),
            "embedding": self.embedding.tolist() if isinstance(self.embedding, np.ndarray) else self.embedding,
       
        }
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "domain": self.domain,
            "platform": self.platform,
            "raw_content": self.raw_content,
            "content": self.content,
            "sentiment_label": self.sentiment_label,
            "sentiment_score": self.sentiment_score,
            "created_at":  self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            "metadata": self.metadata
        }