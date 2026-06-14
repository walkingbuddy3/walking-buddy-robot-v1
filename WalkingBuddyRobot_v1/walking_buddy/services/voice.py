import subprocess


def speak(message):
    print(f"[VOICE] {message}")

    try:
        subprocess.run(
            [
                "espeak",
                "-v", "en-us+f3",
                "-s", "135",
                "-p", "55",
                message,
            ],
            check=True,
        )
        return {
            "ok": True,
            "message": message
        }
    except Exception as exc:
        print(f"[VOICE WARNING] Text-to-speech unavailable: {exc}")
        return {
            "ok": False,
            "message": message,
            "error": str(exc)
        }
