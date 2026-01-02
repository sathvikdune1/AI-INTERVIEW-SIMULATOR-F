import { useEffect, useRef, useState } from "react";
import axios from "axios";
import { speak } from "../utils/speech";
import { startRecording } from "../utils/record";
import { startCamera } from "../utils/camera";
import { loadProctoringModels, analyzeFrame } from "../utils/proctoring";

export default function Interview() {
  const interviewId = localStorage.getItem("interview_id");

  const videoRef = useRef(null);
  const recognitionRef = useRef(null);
  const intervalRef = useRef(null);

  const [question, setQuestion] = useState("");
  const [questionType, setQuestionType] = useState("");
  const [questionNumber, setQuestionNumber] = useState(0);
  const [answer, setAnswer] = useState("");
  const [code, setCode] = useState("");
  const [recording, setRecording] = useState(false);
  const [trustScore, setTrustScore] = useState(100);
  const [warning, setWarning] = useState("");
  const [finished, setFinished] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false); // 🔥 FIX

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

    // reset
    setAnswer("");
    setCode("");
    setRecording(false);
    setIsSubmitting(false); // 🔥 unlock
  };

  /* ---------------- SPEAK ---------------- */
  useEffect(() => {
    if (question && !isCoding) speak(question);
  }, [question, isCoding]);

  /* ---------------- CAMERA ---------------- */
  useEffect(() => {
    const init = async () => {
      await startCamera(videoRef);
      await loadProctoringModels();

      intervalRef.current = setInterval(async () => {
        const result = await analyzeFrame(videoRef.current);
        if (result?.faces.length === 0) {
          setWarning("⚠️ Face not detected");
          setTrustScore((s) => Math.max(s - 2, 0));
        } else {
          setWarning("");
        }
      }, 2000);
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

  /* ---------------- SUBMIT (SAFE) ---------------- */
  const submitAnswer = async () => {
    if (isSubmitting) return; // 🔥 prevent double click

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

  /* ---------------- FINAL STATE ---------------- */
  if (finished) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Finalizing interview…
      </div>
    );
  }

  /* ---------------- UI ---------------- */
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
