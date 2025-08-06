import json
from aiokafka import AIOKafkaConsumer
from typing import AsyncGenerator
from app.core.services.logging_service import LoggingService

logger = LoggingService("KafkaConsumer").get_logger()

class KafkaConsumer:
    def __init__(self, 
            topic: str, 
            bootstrap_servers="localhost:9092", 
            group_id="default-group",
            enable_auto_commit=True,
            max_poll_records=10,
            max_poll_interval_ms=3600000
            ):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            enable_auto_commit=enable_auto_commit,  # disable auto commit to control manually
            session_timeout_ms=30000,        # Default is 10000 (10s) — extend to 30s
            heartbeat_interval_ms=10000,
            max_poll_records=max_poll_records, 
            max_poll_interval_ms=3600000,
	    auto_offset_reset='latest',  
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def get_messages(self) -> AsyncGenerator[dict, None]:
        async for msg in self.consumer:
            try:
                yield msg.value
                # Commit offset only after processing the message successfully
                await self.consumer.commit()
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # optionally decide what to do if processing fails (e.g. break, continue)
    async def commit(self):
        await self.consumer.commit()