from datetime import datetime, timedelta
from typing import List
import numpy as np
from hdbscan import HDBSCAN
from app.core.models.events_models import DetectionContext, Event
from app.core.services.logging_service import LoggingService
from app.detection.base import DetectionStrategy
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


logger = LoggingService("SlidingHDBSCANDetectionStrategy").get_logger()

class HDBSCANDetectionStrategy(DetectionStrategy):
    
    def __init__(self,
                 window_size: int = 80,
                 time_window_days: int = 3,
                 min_cluster_size: int = 5,
                 min_batch_size: int = 50,
                 min_samples: int = 5):
        self.window_size = window_size
        self.time_window_days = time_window_days
        self.min_batch_size = min_batch_size
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples

    async def detect(self, context: DetectionContext) -> DetectionContext:
        logger.info("Running SlidingHDBSCANDetectionStrategy")

        now = datetime.utcnow()
        time_cutoff = now - timedelta(days=self.time_window_days)

        # === STEP 1: Filter old events (keep only ones with recent messages)
        context.current_events = [
            event for event in context.current_events
            if any(m.created_at >= time_cutoff for m in event.messages)
        ]

        # === STEP 2: Combine context messages + recent messages from current events
        messages = context.messages.copy()
        for event in context.current_events:
            messages.extend([m for m in event.messages if m.created_at >= time_cutoff and m.embedding])

        # === STEP 3: Filter messages with valid embeddings
        filtered_msgs = [m for m in messages if m.embedding and len(m.embedding) > 0]

        logger.info(f"Filtered messages (with embeddings): {len(filtered_msgs)}")

        if len(filtered_msgs) < self.min_batch_size:
            logger.info("Not enough messages to cluster.")
            # No clustering, but keep current events as-is
            context.detected_events = []
            context.updated_events = []
            return context

        # === STEP 4: Truncate by window size
        if len(filtered_msgs) > self.window_size:
            filtered_msgs = filtered_msgs[-self.window_size:]

        embeddings = np.array([m.embedding for m in filtered_msgs])

        # === STEP 5: Run clustering with HDBSCAN
        clusterer = HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            metric="cosine",
            algorithm="generic"
        )
        predicted = clusterer.fit_predict(embeddings)

        logger.info(f"Detected clusters: {set(predicted)}")

        # === STEP 6: Group messages by cluster label
        clusters = {}
        for label, msg in zip(predicted, filtered_msgs):
            if label == -1:
                continue  # noise
            clusters.setdefault(label, []).append(msg)

        new_events :List[Event] = []
        updated_events :List[Event]= []
        used_event_ids = set()

        # === STEP 7: Update existing events or create new ones
        for cluster_msgs in clusters.values():
            found_event = None
            for event in context.current_events:
                # If any message of the cluster is in an existing event, update that event
                if any(m in event.messages for m in cluster_msgs):
                    found_event = event
                    break

            if found_event:
                # Merge old + new messages
                found_event.messages = list({*found_event.messages, *cluster_msgs})
                updated_events.append(found_event)
                used_event_ids.add(found_event.id)
            else:
                # Create new event
                new_event = Event.create_from_messages(cluster_msgs)
                new_events.append(new_event)
                used_event_ids.add(new_event.id)

        # === STEP 8: Remove events without recent messages
        final_events :List[Event] = []
        for event in updated_events + new_events:
            event.messages = [m for m in event.messages if m.created_at >= time_cutoff]
            if event.messages:
                final_events.append(event)

        context.current_events = final_events
        context.detected_events = new_events
        context.updated_events = updated_events

        logger.info(f"Detected {len(new_events)} new events, updated {len(updated_events)} events.")
        logger.info(f"Returning total {len(final_events)} current events in context.")

        return context
