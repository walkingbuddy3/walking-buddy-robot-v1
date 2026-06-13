from flask import Flask, jsonify, request, render_template, Response, send_file
import subprocess
from walking_buddy.config import APP_NAME
from walking_buddy.hardware.motors import MotorController
from walking_buddy.services.camera import CameraService
from walking_buddy.services.voice import speak
from walking_buddy.services.obstacles import ObstacleService
from walking_buddy.services.camera_analysis import CameraAnalysisService
from walking_buddy.services.yolo_vision import YoloVisionService


motor_controller = MotorController()
camera_service = CameraService()

def create_app():
    app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

    @app.route("/")
    def index():
        return render_template("index.html", app_name=APP_NAME)

    @app.route("/api/status")
    def status():
        obstacle_status = ObstacleService.get_status()
        return jsonify({
            "ok": True,
            "app": APP_NAME,
            "mode": motor_controller.mode,
            "last_command": motor_controller.last_command,
            "obstacle": obstacle_status
        })

    @app.route("/api/move", methods=["POST"])
    def move():
        data = request.get_json(silent=True) or {}
        command = data.get("command", "").strip().lower()
        seconds = float(data.get("seconds", 0.5))

        result = motor_controller.run_command(command, seconds=seconds)
        return jsonify(result)



    @app.route("/api/emergency-stop", methods=["POST"])
    def emergency_stop():
        result = motor_controller.run_command("stop", seconds=0)
        speak("Emergency stop activated.")
        return jsonify({
            "ok": True,
            "message": "Emergency stop activated.",
            "result": result
        })

    @app.route("/api/obstacle", methods=["GET", "POST"])
    def obstacle():
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            distance = data.get("distance_cm", 100)
            ObstacleService.set_distance(distance)

        return jsonify({
            "ok": True,
            "obstacle": ObstacleService.get_status()
        })

    @app.route("/api/say", methods=["POST"])
    def say():
        data = request.get_json(silent=True) or {}
        message = data.get("message", "Hello, I am Walking Buddy.")
        speak(message)
        return jsonify({"ok": True, "message": message})
    @app.route("/api/camera/latest")
    def latest_camera_image():
        return send_file("/home/walkingbuddy3/camera-tests/latest.jpg", mimetype="image/jpeg")
    @app.route("/video")
    def video():
        return Response(
            camera_service.generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )



    @app.route("/api/camera/capture", methods=["POST"])
    def capture_camera():
        output_file = "/home/walkingbuddy3/camera-tests/latest.jpg"

        result = subprocess.run(
            ["rpicam-still", "-o", output_file, "--nopreview"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "ok": False,
                "message": "Camera capture failed",
                "error": result.stderr
            }), 500

        return jsonify({
            "ok": True,
            "message": "Camera image captured",
            "file": output_file
        })
    @app.route("/api/camera/analyze")
    def analyze_camera():
        return jsonify(CameraAnalysisService.analyze_latest())
    @app.route("/api/vision/detect")
    def vision_detect():
        return jsonify(
            YoloVisionService.analyze_image("/home/walkingbuddy3/camera-tests/latest.jpg")
        )

    return app

