import uuid
from typing import AsyncGenerator, List
from datetime import datetime
from app.core.models.message import Message
from app.kafka.kafka_consumer import KafkaConsumer  # Import KafkaConsumer


class MessageService:
    def __init__(self, kafka_consumer: KafkaConsumer, *args, **kwargs):
        self.kafka_consumer = kafka_consumer  # Inject KafkaConsumer instance

    async def stream_messages(self) -> AsyncGenerator[List[Message], None]:
        # Asynchronously process messages in batches from Kafka
        async for raw_messages in self.kafka_consumer.get_messages():
            # Process each batch of raw messages and convert to Message objects
            messages = [
                Message(
                    id=str(uuid.uuid4()),  # Generate a unique ID
                    platform=raw_message.get('platform', 'dummy'), 
                    platform_id=raw_message.get('platform__id', "1e9cfd36-e1e8-49dc-abe7-d8e983ec2dd3"),   # Kafka as the source
                    domain=raw_message.get('domain', 'default'),  # Default to 'default' if not found
                    source=raw_message.get('source', 'unknown'),  # Default to 'unknown' if not found
                    raw_content=raw_message.get('raw_content', ''),  # Get raw content from Kafka message
                    content=raw_message.get('content', ''),  # Get content from Kafka message
                    sentiment_label=raw_message.get('sentiment_label', 'neutral'),  # Default sentiment label
                    sentiment_score=raw_message.get('sentiment_score', 0.0),  # Default sentiment score
                    created_at= datetime.utcnow(),  # Set the timestamp to current UTC time
                    metadata=raw_message.get('metadata', {})  # Get metadata if available, else default to empty dict
                )
                for raw_message in raw_messages  # Iterate over the batch of messages
            ]
            # print(messages[0].created_at)
            yield messages  # Yield the batch of processed messages
