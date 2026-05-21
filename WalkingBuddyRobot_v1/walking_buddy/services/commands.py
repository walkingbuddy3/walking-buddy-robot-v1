def normalize_voice_command(text):
    text = (text or "").lower().strip()

    if "forward" in text or "go" in text:
        return "forward"
    if "back" in text:
        return "backward"
    if "left" in text:
        return "left"
    if "right" in text:
        return "right"
    if "stop" in text or "halt" in text:
        return "stop"

    return None
