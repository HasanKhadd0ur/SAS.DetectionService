import asyncio
from app.agent import DetectionAgent
from app.core.services.messages_service import MessageService
from app.detection.strategies.hdbscan_detection_strategy import HDBSCANDetectionStrategy
from app.detection.strategies.simple_rule_based import SimpleRuleBased 
from app.kafka.kafka_consumer import KafkaConsumer
from app.pipeline.registry.registry import postprocessing_pipeline,publishing_pipeline

async def main():

    print("[INFO] Detection Service Started")
    consumer = KafkaConsumer("Telegram.Politics",
                             enable_auto_commit=True,
                             max_poll_records=5,
                             max_poll_interval_ms=6000_000)
    
    await consumer.start()  # Start the consumer to begin listening for messages

    print("[INFO] Start Consuming Messages")
    msg_service = MessageService(consumer)


    try :
        
        # Create the detection agent
        detection_agent = DetectionAgent(
            strategy=HDBSCANDetectionStrategy(),  # Use rule-based detection
            min_batch_size=1,
            postprocessing_pipeline=postprocessing_pipeline,
            publishing_pipeline=publishing_pipeline)
        
        

        await detection_agent.handel_messages(msg_service.stream_messages())
    finally:
        await consumer.stop()     
if __name__ == "__main__":
    
    asyncio.run(main())
