import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";
import PageWrapper from "../components/PageWrapper";
import ScoreCard from "../components/ScoreCard";
import ProgressBar from "../components/ProgressBar";

export default function ResultDashboard() {
  const { interviewId } = useParams();
  const [result, setResult] = useState(null);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/api/interview/result/${interviewId}`)
      .then(res => setResult(res.data))
      .catch(err => console.error(err));
  }, [interviewId]);

  if (!result) {
    return <div className="text-white text-center">Loading...</div>;
  }

  return (
    <PageWrapper>
      <div className="p-10 text-white">

        <h1 className="text-4xl font-bold text-center mb-10">
          Interview Analytics Dashboard
        </h1>

        {/* SECTION SCORES */}
        <div className="grid grid-cols-2 gap-6 mb-12">
          {Object.entries(result.scores).map(([k, v]) => {
            if (k === "final") return null;
            return (
              <div key={k} className="glass-card p-4">
                <ScoreCard title={k.toUpperCase()} value={`${v} / 100`} />
                <ProgressBar value={v} max={100} />
              </div>
            );
          })}
        </div>

        {/* PER QUESTION FEEDBACK */}
        {Object.entries(result.feedback).map(([section, items]) => (
          <div key={section} className="mb-10">
            <h2 className="text-2xl font-bold mb-4 capitalize">
              {section.replace("_", " ")} Questions
            </h2>

            {items.map((q, i) => (
              <div key={i} className="glass-card p-4 mb-4">
                <p className="font-semibold mb-2">
                  Q{i + 1}: {q.question}
                </p>
                <p className="text-cyan-400 mb-2">Score: {q.score}/100</p>

                <p><b>Strengths:</b> {q.strengths.join(", ")}</p>
                <p><b>Weaknesses:</b> {q.weaknesses.join(", ")}</p>
                <p><b>Suggestions:</b> {q.suggestions.join(", ")}</p>
              </div>
            ))}
          </div>
        ))}

        {/* FINAL DECISION */}
        <div className="glass-card text-center p-6 mt-10">
          <h2 className="text-2xl mb-2">Final Score</h2>
          <p className="text-4xl font-bold mb-2">
            {result.scores.final} / 100
          </p>
          <p className={`text-3xl font-bold ${
            result.decision === "Selected" ? "text-green-400" : "text-red-400"
          }`}>
            {result.decision}
          </p>
        </div>
      </div>
    </PageWrapper>
  );
}
