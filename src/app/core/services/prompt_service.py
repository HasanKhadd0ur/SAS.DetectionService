class PromptService:
    def __init__(self):
        # You can replace or externalize these if needed
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
                    "تم الإبلاغ عن جريمة قتل في دمشق حيث تم العثور على جثة في الليل، والجهات الأمنية تحقق في الحادثة."
                ),
                "format": (
                    "الرجاء إعادة صياغة المحتوى في فقرة ملخصة وواضحة تحت عنوان:\n"
                    "الملخص:\n"
                )
            }
        }

    def get_prompt_instructions(self, key: str) -> str:
        return self.prompts.get(key, {}).get("instructions", "")

    def get_prompt_illustrations(self, key: str) -> str:
        return self.prompts.get(key, {}).get("illustration", "")

    def get_prompt_format(self, key: str) -> str:
        return self.prompts.get(key, {}).get("format", "")
