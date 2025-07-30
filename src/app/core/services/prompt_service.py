class PromptService:
    def __init__(self):
        # Prompts for different tasks; here focusing on event summarization
        self.prompts = {
            "event_summarization": {
                "instructions": (
                    "أنت مساعد ذكي يقوم بتلخيص أحداث من رسائل متعددة. الهدف هو إنتاج ملخص واضح وموجز يشرح الحدث بطريقة مفهومة."
                ),
                "illustration": (
                    "مثال:\n"
                    "المحتوى:\n"
                    "- تم العثور على جثة في أحد أحياء مدينة دمشق.\n"
                    "- أفاد شهود عيان بأن الجريمة وقعت في منتصف الليل.\n"
                    "- الجهات الأمنية فتحت تحقيقاً في الحادثة.\n\n"
                    "الملخص:\n"
                    "{\n"
                    '  "title": "جريمة قتل في دمشق",\n'
                    '  "summary": "تم الإبلاغ عن جريمة قتل حيث تم العثور على جثة في الليل، والجهات الأمنية تحقق في الحادثة."\n'
                    "}"
                ),
                "format": (
                    "الرجاء إعادة صياغة المحتوى في هيكل JSON واضح بالشكل التالي:\n"
                    "{\n"
                    '  "title": "عنوان الحدث",\n'
                    '  "summary": "ملخص الحدث"\n'
                    "}\n"
                    "يرجى عدم إضافة أي نص آخر خارج هذا الهيكل."
                )
            }
        }

    def get_prompt_instructions(self, key: str) -> str:
        """
        Retrieve the instructions text for a given prompt key.

        Args:
            key (str): The prompt key (e.g., 'event_summarization').

        Returns:
            str: Instructions string, or empty string if not found.
        """
        return self.prompts.get(key, {}).get("instructions", "")

    def get_prompt_illustrations(self, key: str) -> str:
        """
        Retrieve the illustration/example text for a given prompt key.

        Args:
            key (str): The prompt key.

        Returns:
            str: Illustration string, or empty string if not found.
        """
        return self.prompts.get(key, {}).get("illustration", "")

    def get_prompt_format(self, key: str) -> str:
        """
        Retrieve the output format instructions for a given prompt key.

        Args:
            key (str): The prompt key.

        Returns:
            str: Format string, or empty string if not found.
        """
        return self.prompts.get(key, {}).get("format", "")
