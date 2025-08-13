import os
import asyncio
import requests
import jsons
import uuid
import traceback
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

    def is_valid_uuid(self, val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    async def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        if not self.BASE_URL:
            raise ValueError("EVENTS_SERVICE_URL is not set in environment variables")

        for event in detection_context.detected_events:
            if not event.messages:
                logger.warning("Skipping event with no messages.")
                continue

            domain_id = event.messages[0].domainId
            if not domain_id or not self.is_valid_uuid(domain_id):
                logger.error(f"Invalid domainId '{domain_id}' in event. Skipping event.")
                continue

            try:
                lat = float(event.location.latitude)
                lon = float(event.location.longitude)
            except Exception as e:
                logger.error(f"Invalid latitude/longitude for event: {event}. Error: {e}")
                continue

            sentiment = (
                sum(m.sentiment_score for m in event.messages) / len(event.messages)
                if event.messages else 0.0
            )

            event_info = {
                "title": event.title or "",
                "summary": event.summary or "",
                "sentimentScore": sentiment,
                "sentimentLabel": "positive" if sentiment > 0 else "negative",
            }

            topic_name = str(event.topic) if event.topic else "أخبار المحافظات"
            country_name = event.country or ""
            city_name = event.city or ""
            region_name = f"{city_name}, {country_name}" if city_name and country_name else ""

            create_payload = {
                "domainId": domain_id,
                "eventInfo": event_info,
                "topicName": topic_name,
                "countryName": country_name,
                "regionName": region_name,
                "cityName": city_name,
                "latitude": lat,
                "longitude": lon,
            }

            logger.debug(f"Sending payload: {create_payload}")

            try:
                create_response = requests.post(
                    f"{self.BASE_URL}/Events/create",
                    json=create_payload,
                    verify=False
                )
                create_response.raise_for_status()

                event_id = create_response.content.decode('utf-8').strip('"')
                event.id = event_id

                if not event_id:
                    logger.warning("Failed to retrieve event ID after creation.")
                    continue

                logger.info(f"Created event ID: {event_id}")

                message_payload = [m.serialize_message() for m in event.messages]

                await asyncio.sleep(10)  # Don't block the event loop

                if message_payload:
                    bulk_response = requests.post(
                        f"{self.BASE_URL}/events/{event_id}/messages/bulk",
                        json=message_payload,
                        verify=False
                    )
                    bulk_response.raise_for_status()
                    logger.info(f"Added {len(message_payload)} messages to event {event_id}")
                else:
                    logger.info(f"No messages to add for event {event_id}")

            except requests.RequestException as e:
                logger.error(f"Error publishing event: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logger.error(f"Status Code: {e.response.status_code}")
                    logger.error(f"Response Content: {e.response.text}")
                logger.error(f"Payload: {jsons.dumps(create_payload, indent=2)}")
                logger.error(traceback.format_exc())

        if nextStep:
            return await nextStep.process(detection_context)

        return detection_context
