class TrustViolationError(Exception):
    """
    Raised when a trust check fails during model loading.

    Attributes:
        stage (str): The stage at which the violation occurred.
        reason (str): Human-readable reason for the failure.
    """

    def __init__(self, stage: str, reason: str):
        self.stage = stage
        self.reason = reason
        super().__init__(f"[{stage}] {reason}")
