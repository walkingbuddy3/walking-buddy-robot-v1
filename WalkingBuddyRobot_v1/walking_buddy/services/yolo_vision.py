from ultralytics import YOLO

MODEL = YOLO("yolov8n.pt")

HIGH_RISK_OBJECTS = {
    "chair", "couch", "bed", "dining table", "tv", "laptop",
    "backpack", "suitcase", "potted plant"
}

MEDIUM_RISK_OBJECTS = {
    "person", "dog", "cat", "cup", "bottle", "book", "cell phone"
}

CRITICAL_RISK_OBJECTS = {
    "stairs", "car", "truck", "bus", "motorcycle", "bicycle"
}


class YoloVisionService:
    @staticmethod
    def analyze_image(image_path):
        results = MODEL(image_path)
        detections = []

        risk_level = "LOW"
        recommendation = "Path looks clear. Forward movement allowed."
        movement_allowed = True

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = result.names[class_id]
                confidence = float(box.conf[0])

                detections.append({
                    "label": label,
                    "confidence": round(confidence, 2)
                })

                if label in CRITICAL_RISK_OBJECTS:
                    risk_level = "CRITICAL"
                    recommendation = f"Critical obstacle detected: {label}. Stop immediately."
                    movement_allowed = False

                elif label in HIGH_RISK_OBJECTS and risk_level not in ["CRITICAL"]:
                    risk_level = "HIGH"
                    recommendation = f"Obstacle detected: {label}. Do not move forward."
                    movement_allowed = False

                elif label in MEDIUM_RISK_OBJECTS and risk_level not in ["CRITICAL", "HIGH"]:
                    risk_level = "MEDIUM"
                    recommendation = f"Object detected: {label}. Move with caution."
                    movement_allowed = True

        return {
            "ok": True,
            "detections": detections,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "movement_allowed": movement_allowed
        }
