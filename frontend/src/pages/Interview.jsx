import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { speak } from "../utils/speech";
import { startRecording } from "../utils/record";
import { startCamera } from "../utils/camera";
import { loadProctoringModels, analyzeFrame } from "../utils/proctoring";
import { analyzeVision } from "../api/interviewApi";

export default function Interview() {
  const interviewId = localStorage.getItem("interview_id");

  const videoRef = useRef(null);
  const recognitionRef = useRef(null);
  const intervalRef = useRef(null);
  const noFaceCounter = useRef(0);

  const [question, setQuestion] = useState("");
  const [questionType, setQuestionType] = useState("");
  const [questionNumber, setQuestionNumber] = useState(0);
  const [answer, setAnswer] = useState("");
  const [code, setCode] = useState("");
  const [recording, setRecording] = useState(false);
  const [trustScore, setTrustScore] = useState(100);
  const [warning, setWarning] = useState("");
  const [finished, setFinished] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isCoding = questionType === "coding";

  /* ---------------- LOAD QUESTION ---------------- */
  const loadQuestion = async () => {
    const res = await axios.post(
      "http://127.0.0.1:8000/api/interview/next-question",
      new URLSearchParams({ interview_id: interviewId })
    );

    if (res.data.message === "Interview completed") {
      setFinished(true);

      await axios.post(
        "http://127.0.0.1:8000/api/interview/evaluate",
        new URLSearchParams({ interview_id: interviewId })
      );

      window.location.href = `/result/${interviewId}`;
      return;
    }

    setQuestion(res.data.question);
    setQuestionType(res.data.question_type);
    setQuestionNumber(res.data.question_number);

    setAnswer("");
    setCode("");
    setRecording(false);
    setIsSubmitting(false);
  };

  /* ---------------- SPEAK ---------------- */
  useEffect(() => {
    if (question && !isCoding) speak(question);
  }, [question, isCoding]);

  /* ---------------- CAMERA + PROCTORING ---------------- */
  useEffect(() => {
    const init = async () => {
      await startCamera(videoRef);
      await loadProctoringModels();

      intervalRef.current = setInterval(async () => {
        const video = videoRef.current;
        if (!video || video.readyState < 2) return;

        /* -------- FRONTEND FACE CHECK -------- */
        const result = await analyzeFrame(video);

        if (result?.faces.length === 0) {
          noFaceCounter.current += 1;

          if (noFaceCounter.current >= 2) {
            setWarning("⚠️ Face not detected");
            setTimeout(() => setWarning(""), 2500);

            setTrustScore(prev => Math.max(prev - 2, 0));
          }

        } else if (result?.faces.length === 1) {
          noFaceCounter.current = 0;
        }

        /* -------- BACKEND VISION CHECK -------- */
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        const imageBase64 = canvas.toDataURL("image/jpeg");

        try {
          const response = await analyzeVision(imageBase64);
          const data = response.data;

          let deduction = 0;

          if (data.emotion === "no_face") {
            deduction = 5;
            setWarning("⚠️ Face not detected");
            setTimeout(() => setWarning(""), 2500);
          }

          else if (data.objects_detected?.includes("cell phone")) {
            deduction = 5;
            setWarning("⚠️ Mobile phone detected");
            setTimeout(() => setWarning(""), 2500);
          }

          else if (data.objects_detected?.includes("book")) {
            deduction = 3;
            setWarning("⚠️ Book detected");
            setTimeout(() => setWarning(""), 2500);
          }

          if (deduction > 0) {
            setTrustScore(prev => {
              const newScore = Math.max(prev - deduction, 0);

              if (newScore < 30) {
                alert("Interview terminated due to suspicious activity.");
                window.location.href = "/";
              }

              return newScore;
            });
          }

        } catch (err) {
          console.error("Vision error:", err);
        }

      }, 1500);
    };

    init();
    loadQuestion();

    return () => clearInterval(intervalRef.current);
  }, []);

  /* ---------------- RECORD ---------------- */
  const handleRecord = () => {
    if (recording) {
      recognitionRef.current?.stop();
      setRecording(false);
      return;
    }

    recognitionRef.current = startRecording((text) => {
      setAnswer(text);
      setRecording(false);
    });

    setRecording(true);
  };

  /* ---------------- SUBMIT ---------------- */
  const submitAnswer = async () => {
    if (isSubmitting) return;

    setIsSubmitting(true);

    const payload = new URLSearchParams({
      interview_id: interviewId,
      question,
      question_type: questionType,
      answer: isCoding ? code : answer
    });

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/interview/submit-answer",
        payload
      );
      await loadQuestion();
    } catch (err) {
      console.error(err);
      setIsSubmitting(false);
    }
  };

  if (finished) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Finalizing interview…
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-black text-white flex justify-center items-center">
      <video
        ref={videoRef}
        autoPlay
        muted
        className="fixed top-6 right-6 w-56 h-40 border rounded"
      />

      <div className="w-[900px] bg-black/60 rounded-xl p-6">
        <div className="flex justify-between mb-4">
          <span>Question {questionNumber}</span>
          <span>Trust Score: {trustScore}</span>
        </div>

        {warning && (
          <div className="bg-red-600 p-2 rounded mb-3">{warning}</div>
        )}

        <p className="text-xl mb-4">{question}</p>

        {!isCoding ? (
          <textarea
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            rows={4}
            className="w-full p-3 text-black mb-4"
          />
        ) : (
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={14}
            className="w-full p-3 text-black font-mono mb-4"
          />
        )}

        <div className="flex gap-3">
          {!isCoding && (
            <button
              onClick={handleRecord}
              disabled={isSubmitting}
              className="bg-green-600 px-4 py-2 rounded disabled:opacity-50"
            >
              {recording ? "Stop" : "🎤 Record"}
            </button>
          )}

          <button
            onClick={() => {
              setAnswer("");
              setCode("");
            }}
            disabled={isSubmitting}
            className="bg-yellow-500 px-4 py-2 rounded text-black disabled:opacity-50"
          >
            Clear
          </button>

          <button
            onClick={submitAnswer}
            disabled={isSubmitting}
            className="bg-indigo-600 px-6 py-2 rounded disabled:opacity-50"
          >
            {isSubmitting ? "Submitting..." : "Submit & Next"}
          </button>
        </div>
      </div>
    </div>
  );
}