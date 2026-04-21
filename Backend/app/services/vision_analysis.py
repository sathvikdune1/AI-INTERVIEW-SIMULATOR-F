from deepface import DeepFace
from ultralytics import YOLO
import cv2

# Load YOLO model once
yolo_model = YOLO("yolov8n.pt")

# Suspicious objects
SUSPICIOUS_OBJECTS = [
    "cell phone",
    "book",
    "laptop",
    "clock"
]

def analyze_frame(frame):

    try:

        trust_score = 100
        confidence_score = 50
        emotion = "unknown"
        detected_objects = []
        face_status = "single_face"

        # =============================
        # FACE + EMOTION ANALYSIS
        # =============================

        analysis = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=False
        )

        if isinstance(analysis, list):

            if len(analysis) == 0:
                face_status = "no_face"
                emotion = "no_face"
                trust_score -= 10

            elif len(analysis) > 1:
                face_status = "multiple_faces"
                emotion = "multiple_faces"
                trust_score -= 15

            else:
                emotion = analysis[0]["dominant_emotion"]
                face_status = "single_face"

        # =============================
        # OBJECT DETECTION
        # =============================

        results = yolo_model(frame, verbose=False)

        for r in results:
            for box in r.boxes:

                cls_id = int(box.cls[0])
                label = yolo_model.names[cls_id]

                if label in SUSPICIOUS_OBJECTS:
                    detected_objects.append(label)

        detected_objects = list(set(detected_objects))

        # =============================
        # TRUST SCORE DEDUCTIONS
        # =============================

        if "cell phone" in detected_objects:
            trust_score -= 20

        if "book" in detected_objects:
            trust_score -= 10

        if "laptop" in detected_objects:
            trust_score -= 10

        if "clock" in detected_objects:
            trust_score -= 5

        if emotion in ["fear", "sad"]:
            confidence_score -= 5

        trust_score = max(trust_score, 0)
        confidence_score = max(confidence_score, 0)

        return {
            "trust_score": trust_score,
            "confidence_score": confidence_score,
            "emotion": emotion,
            "face_status": face_status,
            "objects_detected": detected_objects
        }

    except Exception as e:

        return {
            "trust_score": 20,
            "confidence_score": 20,
            "emotion": "error",
            "face_status": "error",
            "objects_detected": []
        }