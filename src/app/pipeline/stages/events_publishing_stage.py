import os
from time import sleep
import requests
import jsons
jsons.suppress_warnings(True)
from typing import Optional
from dotenv import load_dotenv
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext

# Load environment variables from .env
load_dotenv()

class EventsPublishingStage(ProcessingStage):
    BASE_URL = os.getenv("server_ul")  # Load from .env

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        if not self.BASE_URL:
            raise ValueError("EVENTS_SERVICE_URL is not set in environment variables")
        

        for event in detection_context.detected_events:
    
            sentiment = sum( [m.sentiment_score for m in  event.messages] ) / len (event.messages) if len(event.messages ) >0 else 0 

            create_payload = {
                "eventInfo": {
                    "summary": event.summary,
                    "title": event.messages[0].content[:170] if event.messages and event.messages[0].content else "no title",
                    "sentimentScore": sentiment ,
                    "sentimentLabel": "negative" if sentiment <=0  else "positive",
                    "time": event.time.isoformat() if event.time else None
                    
                },
                "topicName": "أخبار سياسية سورية",
                "countryName": "سوريا",
                "regionName": str(event.location_name),
                "cityName": "سوريا",
                "latitude": event.location.latitude,
                "longitude": event.location.longitude
            }

            try:
                create_response = requests.post(f"{self.BASE_URL}/Events/create", json=create_payload,verify=False)
                create_response.raise_for_status()
               
                event_id = create_response.content.decode('utf-8').strip('"')
                event.id=event_id
                
                if not event_id:
                    print("[!] Failed to retrieve event ID after creation.")
                    continue

                print(f"[+] Created event ID: {event_id}")

                # message_payload = [asdict(msg) for msg in event.messages]
                message_payload = [m.serialize_message() for m in event.messages]
                sleep(10)
                # if message_payload:
                    # bulk_response = requests.post(f"{self.BASE_URL}/events/{event_id}/messages/bulk", json=message_payload,verify=False)
                    # print(bulk_response.text)
               
                    # bulk_response.raise_for_status()
                    
                    # print(f"[+] Added {len(message_payload)} messages to event {event_id}")
                # else:
                    # print(f"[~] No messages to add for event {event_id}")

            except requests.RequestException as e:
                print(f"[!] Error publishing event: {e}")

        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
