from app.core.configs.app_config import ALLOWED_RULES
from app.core.models.policy_rule import PolicyRule

class PolicyService:
    def __init__(self):
        self.rules = {
            name: PolicyRule(
                name=name,
                value=rule["default"],
                description=rule.get("description", "")
            )
            for name, rule in ALLOWED_RULES.items()
        }

    def get_all_rules(self):
        return [rule.to_dict() for rule in self.rules.values()]

    def get_rule(self, name: str):
        rule = self.rules.get(name)
        if rule is None:
            raise ValueError(f"Rule '{name}' not found.")
        return rule.to_dict()

    def update_rule(self, name: str, value):
        if name not in ALLOWED_RULES:
            raise ValueError(f"Invalid rule name '{name}'.")

        expected_type = ALLOWED_RULES[name]["type"]
        if not isinstance(value, expected_type):
            try:
                value = expected_type(value)
            except Exception:
                raise TypeError(f"Value for '{name}' must be of type {expected_type.__name__}")

        self.rules[name].value = value
        return self.rules[name].to_dict()
    def toggle_rule(self, name: str, enabled: bool):
        if name not in self.rules:
            raise ValueError(f"Rule '{name}' not found.")
        self.rules[name].enabled = enabled
        return self.rules[name].to_dict()

# Singleton instance
policy_service = PolicyService()
