import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/interview",
});

export const startInterview = (data) =>
  API.post("/start", data, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

export const uploadResume = (data) =>
  API.post("/upload-resume", data);

export const generateQuestions = (data) =>
  API.post("/generate-questions", data);

export const nextQuestion = (data) =>
  API.post("/next-question", data);

export const submitAnswer = (data) =>
  API.post("/submit-answer", data);

export const evaluateInterview = (data) =>
  API.post("/evaluate", data);
