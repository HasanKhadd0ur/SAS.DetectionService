from typing import Optional
from app.core.configs.base_config import BaseConfig
from app.core.services.location_inference_service import LocationInferenceService
from app.core.models.events_models import DetectionContext
from app.core.services.logging_service import LoggingService
from app.pipeline.base.base import ProcessingStage

import requests

logger = LoggingService("DetectionAgent").get_logger()

class EventsLocatingStage(ProcessingStage):
    
    def __init__(self,config: BaseConfig, location_service: LocationInferenceService):
        self.location_service = location_service
        self.nominatim_url = "https://nominatim.openstreetmap.org/reverse"
        self.user_agent = config.get_random_user_agent()

    def get_city_country_from_coords(self, latitude: float, longitude: float) -> dict:
        """
        Use Nominatim API to reverse geocode latitude and longitude to city and country.

        Returns a dict like: {"city": "...", "country": "..."}
        """
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "addressdetails": 1,
            "zoom": 10  # zoom level controls granularity; 10 is roughly city level
        }
        headers = {
            "User-Agent": self.user_agent
        }

        response = requests.get(self.nominatim_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        address = data.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village") or ""
        country = address.get("country", "")

        return {
            "city": city,
            "country": country
        }

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        for event in detection_context.detected_events:
            try:
                location_name='سوريا دمشق'
                # Extract textual location name from event using your location service
                location_name = self.location_service.extract_event_location(event)
                event.location_name = location_name
                logger.info(f"Extracted location name '{location_name}' for event {getattr(event, 'id', 'unknown')}")

                # Geocode textual location name to get coordinates (if available)
                geocoded_location = self.location_service.geocode(location_name)
                event.location = geocoded_location
                logger.info(f"Geocoded location for event {getattr(event, 'id', 'unknown')}: {geocoded_location}")

                # Now use Nominatim reverse geocoding on the coordinates
                lat = getattr(event.location, "latitude", None)
                lon = getattr(event.location, "longitude", None)

                if lat is not None and lon is not None:
                    city_country = self.get_city_country_from_coords(lat, lon)
                    event.city = city_country.get("city", "")
                    event.country = city_country.get("country", "")
                    logger.info(
                        f"Nominatim reverse geocoded city '{event.city}', country '{event.country}' for event {getattr(event, 'id', 'unknown')}"
                    )
                else:
                    logger.warning(f"No valid coordinates for reverse geocoding for event {getattr(event, 'id', 'unknown')}")
                    event.city = ""
                   

            except Exception as e:
                logger.error(f"Failed to extract or geocode location for event {getattr(event, 'id', 'unknown')}: {e}")
                event.location_name = location_name
                # event.location = location
                event.city = "سوريا"
                event.country = "دمشق"

        if nextStep:
            return nextStep.process(detection_context)
        return detection_context