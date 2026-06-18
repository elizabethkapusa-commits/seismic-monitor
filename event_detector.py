# Simple event detector for seismic samples


def detect_event(sample_value, threshold):
    """
    Detects whether a sample exceeds the event threshold.
    """

    if abs(sample_value) >= threshold:
        return True

    return False


def get_event_status(sample_value, threshold):
    """
    Returns a readable event status.
    """

    if detect_event(sample_value, threshold):
        return "EVENT_DETECTED"

    return "NORMAL"