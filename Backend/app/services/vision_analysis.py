import cv2
import mediapipe as mp

mp_face = mp.solutions.face_mesh.FaceMesh()

def analyze_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_face.process(rgb)
    return 85 if result.multi_face_landmarks else 40
