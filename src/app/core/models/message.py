from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    id:str=""
    source: str=""
    domain: str=""
    platform: str=""
    raw_content: str=""
    content: str=""
    sentiment_label: str=""
    sentiment_score: float =0
    platform_id:str=" 1e9cfd36-e1e8-49dc-abe7-d8e983ec2dd3"
    created_at: datetime = datetime.utcnow()
    metadata: dict = None

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
            "sentimentScore": str(self.sentiment_score)
        }
