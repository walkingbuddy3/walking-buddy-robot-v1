from flask import Flask, render_template, jsonify, request, Response
from walking_buddy.config import APP_NAME
from walking_buddy.hardware.motors import MotorController
from walking_buddy.services.camera import CameraService
from walking_buddy.services.voice import speak

motor_controller = MotorController()
camera_service = CameraService()

def create_app():
    app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

    @app.route("/")
    def index():
        return render_template("index.html", app_name=APP_NAME)

    @app.route("/api/status")
    def status():
        return jsonify({
            "ok": True,
            "app": APP_NAME,
            "mode": motor_controller.mode,
            "last_command": motor_controller.last_command
        })

    @app.route("/api/move", methods=["POST"])
    def move():
        data = request.get_json(silent=True) or {}
        command = data.get("command", "").strip().lower()
        seconds = float(data.get("seconds", 0.5))

        result = motor_controller.run_command(command, seconds=seconds)
        return jsonify(result)

    @app.route("/api/say", methods=["POST"])
    def say():
        data = request.get_json(silent=True) or {}
        message = data.get("message", "Hello, I am Walking Buddy.")
        speak(message)
        return jsonify({"ok": True, "message": message})

    @app.route("/video")
    def video():
        return Response(
            camera_service.generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )

    return app
