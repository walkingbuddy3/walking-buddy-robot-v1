from ultralytics import YOLO

MODEL = YOLO("yolov8n.pt")

class YoloVisionService:
    @staticmethod
    def analyze_image(image_path):
        results = MODEL(image_path)
        detections = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = result.names[class_id]
                confidence = float(box.conf[0])

                detections.append({
                    "label": label,
                    "confidence": round(confidence, 2)
                })

        return {
            "ok": True,
            "detections": detections
        }
