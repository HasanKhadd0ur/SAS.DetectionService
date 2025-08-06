from typing import Optional
from app.core.configs.base_config import BaseConfig
from app.core.services.prompt_service import PromptService
from app.pipeline.base.base import ProcessingStage
from app.core.models.events_models import DetectionContext
from app.core.configs.env_config import EnvConfig
import google.generativeai as genai
import re
import json

MAX_SUMMARY_LENGTH = 255

class EventsSummerizationStage(ProcessingStage):
    def __init__(self, config: BaseConfig):
        # Initialize PromptService for prompt templates
        self.prompt_service = PromptService()
        self.config = config

        # Configure Gemini AI client with API key from config
        api_key = self.config.get_api_key()
        genai.configure(api_key=api_key)

        # Initialize the Gemini generative model
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        for event in detection_context.detected_events:
            try:
                # Combine all event messages into a single string
                all_messages_text = "\n".join([msg.content for msg in event.messages])

                # Truncate text to max allowed length to avoid too long prompts
                if len(all_messages_text) > MAX_SUMMARY_LENGTH:
                    all_messages_text = all_messages_text[:MAX_SUMMARY_LENGTH]

                # Get prompt parts: instructions, examples, and format spec
                instructions = self.prompt_service.get_prompt_instructions("event_summarization")
                examples = self.prompt_service.get_prompt_illustrations("event_summarization")
                format_spec = self.prompt_service.get_prompt_format("event_summarization")

                # Build full prompt text for the LLM
                prompt = (
                    f"{instructions}\n\n"
                    f"{examples}\n\n"
                    f"{format_spec}\n\n"
                    f"المحتوى:\n{all_messages_text}"
                )

                # Generate content from Gemini model using the full prompt
                response = self.model.generate_content(prompt)

                # The raw text response from the LLM (expected to be a JSON string)
                raw_output = response.text.strip()

                # Clean up code fences if present (optional, depending on LLM output)
                raw_output = re.sub(r"```(?:\w+)?\n(.*?)\n```", r"\1", raw_output, flags=re.DOTALL).strip()

                # Attempt to parse the LLM output as JSON with 'title' and 'summary' keys
                try:
                    parsed = json.loads(raw_output)
                    event.title = parsed.get("title", "").strip()
                    event.summary = parsed.get("summary", "").strip()
                except json.JSONDecodeError:
                    # Fallback: if JSON parsing fails, store raw output as summary and empty title
                    # event.title = ""
                    # event.summary = raw_output
                    event.title = all_messages_text[:50].strip()  # example: first 50 chars as title
                    event.summary = all_messages_text


                # # For now, just assign the truncated messages text as summary and title
                # event.title = all_messages_text[:50].strip()  # example: first 50 chars as title
                # event.summary = all_messages_text

            except Exception as e:
                # If anything goes wrong, mark summary as failed and include error message
                # print(all_messages_text)
                event.title = all_messages_text[:50].strip()  # example: first 50 chars as title
                event.summary = all_messages_text

        # If there is a next pipeline stage, continue processing
        if nextStep:
            return nextStep.process(detection_context)

        # Return the updated detection context with summaries and titles added
        return detection_context

