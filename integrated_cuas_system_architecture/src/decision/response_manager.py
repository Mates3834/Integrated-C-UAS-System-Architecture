def select_response(risk_level):
    """
    Abstract safety workflow only; intentionally excludes engagement actions.
    """
    return {
        "UNKNOWN": "MONITOR",
        "LOW": "MONITOR",
        "MEDIUM": "VERIFY",
        "HIGH": "ALERT",
    }.get(risk_level, "MONITOR")
