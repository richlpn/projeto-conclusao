class RuleException(Exception):
    """Base class for business rule exceptions."""

    def __init__(self, rule_name, message, data=None):
        self.rule_name = rule_name
        self.message = message
        self.data = data
        super().__init__(f"Rule '{rule_name}' violated: {message}")
