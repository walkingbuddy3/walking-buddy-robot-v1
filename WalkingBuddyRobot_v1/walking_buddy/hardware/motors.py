from time import sleep
from walking_buddy import config

class MotorController:
    def __init__(self):
        self.safe_mode = config.SAFE_MODE
        self.mode = "SAFE_SIMULATION" if self.safe_mode else "GPIO_HARDWARE"
        self.last_command = "none"

        if not self.safe_mode:
            self._setup_gpio()

    def _setup_gpio(self):
        # Hardware mode will be completed after we confirm the exact motor controller.
        # This prevents accidental wheel movement before wiring is verified.
        raise NotImplementedError(
            "Hardware GPIO mode is not enabled yet. Keep SAFE_MODE=True until wiring is confirmed."
        )

    def _validate_seconds(self, seconds):
        seconds = max(0.1, min(float(seconds), config.MAX_MOVE_SECONDS))
        return seconds

    def run_command(self, command, seconds=None):
        seconds = self._validate_seconds(seconds or config.DEFAULT_MOVE_SECONDS)

        allowed = {
            "forward": self.forward,
            "backward": self.backward,
            "left": self.left,
            "right": self.right,
            "stop": self.stop
        }

        if command not in allowed:
            return {
                "ok": False,
                "error": f"Unknown command: {command}",
                "allowed": list(allowed.keys())
            }

        allowed[command](seconds=seconds)
        return {
            "ok": True,
            "command": command,
            "seconds": seconds,
            "mode": self.mode
        }

    def forward(self, seconds=0.5):
        self.last_command = "forward"
        self._simulate("Moving forward", seconds)

    def backward(self, seconds=0.5):
        self.last_command = "backward"
        self._simulate("Moving backward", seconds)

    def left(self, seconds=0.5):
        self.last_command = "left"
        self._simulate("Turning left", seconds)

    def right(self, seconds=0.5):
        self.last_command = "right"
        self._simulate("Turning right", seconds)

    def stop(self, seconds=0):
        self.last_command = "stop"
        self._simulate("Stopping", 0)

    def _simulate(self, action, seconds):
        if self.safe_mode:
            print(f"[SAFE MODE] {action} for {seconds} seconds")
            if seconds:
                sleep(seconds)
        else:
            # Real motor commands will go here after hardware arrives.
            pass
