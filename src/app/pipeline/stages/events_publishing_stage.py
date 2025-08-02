import os
from time import sleep
import requests
import jsons
jsons.suppress_warnings(True)
from typing import Optional
from dotenv import load_dotenv
from app.pipeline.base.base import ProcessingStage
from app.core.models.events_models import DetectionContext
from app.core.services.logging_service import LoggingService

# Load environment variables from .env
load_dotenv()

logger = LoggingService("EventsPublishingStage").get_logger()

class EventsPublishingStage(ProcessingStage):
    BASE_URL = os.getenv("server_ul")  # Load from .env

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        if not self.BASE_URL:
            raise ValueError("EVENTS_SERVICE_URL is not set in environment variables")

        for event in detection_context.detected_events:
            sentiment = (
                sum([m.sentiment_score for m in event.messages]) / len(event.messages)
                if len(event.messages) > 0
                else 0
            )

            create_payload = {
                "eventInfo": {
                    "summary": event.summary,
                    "title": event.title,
                    "sentimentScore": sentiment,
                    "sentimentLabel": "negative" if sentiment <= 0 else "positive",
                    "time": event.time.isoformat() if event.time else None
                },
                "topicName": str(event.topic),
                "countryName":event.country,
                "regionName": str(event.city + ', '+event.country),
                "cityName": event.city,
                "latitude": event.location.latitude,
                "longitude": event.location.longitude
            }

            try:
                create_response = requests.post(f"{self.BASE_URL}/Events/create", json=create_payload, verify=False)
                create_response.raise_for_status()

                event_id = create_response.content.decode('utf-8').strip('"')
                event.id = event_id

                if not event_id:
                    logger.warning("Failed to retrieve event ID after creation.")
                    continue

                logger.info(f"Created event ID: {event_id}")

                message_payload = [m.serialize_message() for m in event.messages]
                sleep(10)

                # Uncomment to send messages later
                if message_payload:
                    bulk_response = requests.post(f"{self.BASE_URL}/events/{event_id}/messages/bulk", json=message_payload, verify=False)
                    bulk_response.raise_for_status()
                    logger.info(f"Added {len(message_payload)} messages to event {event_id}")
                else:
                    logger.info(f"No messages to add for event {event_id}")

            except requests.RequestException as e:
                logger.error(f"Error publishing event: {e}")
                logger.error(f"Payload: {jsons.dumps(create_payload, indent=2)}")


        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
