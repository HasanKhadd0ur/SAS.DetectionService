class PolicyRule:
    def __init__(self, name: str, value, description: str = "", enabled: bool = True):
        self.name = name
        self.value = value
        self.description = description
        self.enabled = enabled  # Add this flag

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "description": self.description,
            "enabled": self.enabled  # Include it in API
        }
