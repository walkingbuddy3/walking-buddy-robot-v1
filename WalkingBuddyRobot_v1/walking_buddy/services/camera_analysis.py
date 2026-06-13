import os
from PIL import Image, ImageStat

LATEST_IMAGE = "/home/walkingbuddy3/camera-tests/latest.jpg"

class CameraAnalysisService:
    @staticmethod
    def analyze_latest():
        if not os.path.exists(LATEST_IMAGE):
            return {
                "ok": False,
                "message": "No camera image found yet"
            }

        image = Image.open(LATEST_IMAGE).convert("L")
        stat = ImageStat.Stat(image)
        brightness = stat.mean[0]

        obstacle_possible = brightness < 35

        return {
            "ok": True,
            "brightness": round(brightness, 2),
            "obstacle_possible": obstacle_possible,
            "message": "Obstacle possible or camera covered" if obstacle_possible else "Path looks clear"
        }
