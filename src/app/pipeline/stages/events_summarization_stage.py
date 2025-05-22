from typing import Optional
from app.core.configs.base_config import BaseConfig
from app.core.services.prompt_service import PromptService
from app.pipeline.base import ProcessingStage
from app.core.models.events_models import DetectionContext
from app.core.configs.env_config import EnvConfig
import google.generativeai as genai
import re

class EventsSummerizationStage(ProcessingStage):
    def __init__(self,config :BaseConfig):
        self.prompt_service = PromptService()
        self.config = config
        api_key =self.config.get_api_key()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def process(self, detection_context: DetectionContext, nextStep: Optional[ProcessingStage] = None) -> DetectionContext:
        for event in detection_context.detected_events:
            try:
                # Combine all messages into one block of text
                all_messages_text = "\n".join([msg.content for msg in event.messages])

                # Load the prompt template
                instructions = self.prompt_service.get_prompt_instructions("event_summarization")
                examples = self.prompt_service.get_prompt_illustrations("event_summarization")
                format_spec = self.prompt_service.get_prompt_format("event_summarization")

                # prompt = f"{instructions}\n\n{examples}\n\n{format_spec}\n\nالمحتوى:\n{all_messages_text}"

                # Generate the summary
                # response = self.model.generate_content(prompt)
                # summary = response.text.strip()
                summary = all_messages_text
                # Clean up if it includes markdown fencing
                summary = re.sub(r"```(?:\w+)?\n(.*?)\n```", r"\1", summary, flags=re.DOTALL).strip()
                # print(all_messages_text +"\n\n\n\n")
                # print(summary)

                event.summary = summary

            except Exception as e:
                event.summary = f"LLM summarization failed: {e}"

        # Proceed to next stage if any
        if nextStep:
            return nextStep.process(detection_context)

        return detection_context
