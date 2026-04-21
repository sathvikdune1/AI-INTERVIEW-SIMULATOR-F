import * as faceapi from "face-api.js";

let modelsLoaded = false;

export async function loadProctoringModels() {
  if (modelsLoaded) return;

  const MODEL_URL = "/models";

  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
    faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL)
  ]);

  modelsLoaded = true;
}

export async function analyzeFrame(video) {

  if (!video || !video.srcObject || video.readyState < 2) {
    return { cameraLost: true };
  }

  const detections = await faceapi
    .detectAllFaces(
      video,
      new faceapi.TinyFaceDetectorOptions({
        inputSize: 512,
        scoreThreshold: 0.25
      })
    )
    .withFaceLandmarks(true);

  let headStatus = "OK";

  if (detections.length === 1) {
    const landmarks = detections[0].landmarks;
    const nose = landmarks.getNose();
    const leftEye = landmarks.getLeftEye();
    const rightEye = landmarks.getRightEye();

    const noseX = nose[3].x;
    const midEyeX = (leftEye[0].x + rightEye[3].x) / 2;

    if (noseX < midEyeX - 18) headStatus = "Looking Right";
    else if (noseX > midEyeX + 18) headStatus = "Looking Left";
  }

  return {
    cameraLost: false,
    faces: detections,
    headStatus
  };
}