from walking_buddy.services.commands import normalize_voice_command

def test_commands():
    assert normalize_voice_command("go forward") == "forward"
    assert normalize_voice_command("turn left") == "left"
    assert normalize_voice_command("stop now") == "stop"
