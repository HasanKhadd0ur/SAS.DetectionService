import asyncio
from app.agent import DetectionAgent
from app.core.services.messages_service import MessageService
from app.detection.strategies.simple_rule_based import SimpleRuleBased 
from app.kafka.kafka_consumer import KafkaConsumer
from app.pipeline.registry import postprocessing_pipeline,publishing_pipeline

async def main():

    print("[+] Detection Service Started")
    consumer = KafkaConsumer("telegram.Politics")
    
    await consumer.start()  # Start the consumer to begin listening for messages

    print("[+] Start Consuming Messages")
    msg_service = MessageService(consumer)


    # Create the detection agent
    detection_agent = DetectionAgent(
        detection_strategy=SimpleRuleBased(),  # Use rule-based detection
        postprocessing_pipeline=postprocessing_pipeline,
        publishing_pipeline=publishing_pipeline
    )


    await detection_agent.run(msg_service.stream_messages())

if __name__ == "__main__":
    
    asyncio.run(main())
