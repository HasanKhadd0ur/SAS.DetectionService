import asyncio
from threading import Thread
from app.agent import DetectionAgent
from app.core.services.messages_service import MessageService
from app.detection.registry.register_strategies import register_strategies
from app.detection.factory.strategy_factory import StrategyFactory
from app.detection.factory.detection_config import DetectionConfigManager
from app.kafka.kafka_consumer import KafkaConsumer
from app.pipeline.factory.default_pipelines import postprocessing_pipeline, publishing_pipeline
from app.routes.config_routes import app as flask_app
import uuid

def start_flask():
    flask_app.run(host="0.0.0.0", port=5300)

async def run_detection_loop():
    print("[INFO] Detection Service Started")
    consumer = KafkaConsumer("Telegram.Politics",
                             group_id='scraper-260e8ee0-14db-448b-a466-250ad6667be3',#'scraper-' + str(uuid.uuid4()),
                             enable_auto_commit=True,
                             max_poll_records=5,
                             max_poll_interval_ms=6000_000)
    
    await consumer.start()
    
    strategy = DetectionConfigManager.get_current_strategy()
   
    detection_agent = DetectionAgent(
        strategy=strategy,
        min_batch_size=1,
        postprocessing_pipeline=postprocessing_pipeline,
        publishing_pipeline=publishing_pipeline)

    print("[INFO] Start Consuming Messages")
    msg_service = MessageService(consumer)

    try:
        
        curr_strategy = DetectionConfigManager.get_current_strategy()
        
        detection_agent.set_detection_strategy(strategy=curr_strategy)
        
        await detection_agent.handel_messages(msg_service.stream_messages())
    finally:
        await consumer.stop()

async def main():
    register_strategies()
    initial_strategy = StrategyFactory.create_strategy("hdbscan")
    DetectionConfigManager.set_strategy("hdbscan", initial_strategy)

    flask_thread = Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    await run_detection_loop()

if __name__ == "__main__":
    asyncio.run(main())
