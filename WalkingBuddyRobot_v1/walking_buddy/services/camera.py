import cv2
from walking_buddy import config

class CameraService:
    def __init__(self):
        self.camera_index = config.CAMERA_INDEX

    def generate_frames(self):
        camera = cv2.VideoCapture(self.camera_index)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

        if not camera.isOpened():
            while True:
                frame = self._error_frame("Camera not available yet")
                ok, buffer = cv2.imencode(".jpg", frame)
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"

        while True:
            success, frame = camera.read()
            if not success:
                break

            cv2.putText(
                frame,
                "Walking Buddy Camera",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

            ok, buffer = cv2.imencode(".jpg", frame)
            if not ok:
                continue

            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"

        camera.release()

    def _error_frame(self, message):
        import numpy as np
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, message, (40, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        return frame
