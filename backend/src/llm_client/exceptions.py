class DomainMismatchException(Exception):
    """
    Raised when there is a mismatch in the domain or configuration
    of the LLM client or prompt.
    """
    def __init__(self, message: str = "Domain mismatch occurred", *args):
        # Call the base class constructor
        super().__init__(message, *args)
        self.message = message

    def __str__(self):
        return f"DomainMismatchException: {self.message}"