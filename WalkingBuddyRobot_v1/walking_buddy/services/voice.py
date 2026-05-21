def speak(message):
    print(f"[VOICE] {message}")

    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except Exception as exc:
        print(f"[VOICE WARNING] Text-to-speech unavailable: {exc}")
