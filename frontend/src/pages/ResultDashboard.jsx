import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import PageWrapper from "../components/PageWrapper";
import ScoreCard from "../components/ScoreCard";
import ProgressBar from "../components/ProgressBar";

export default function ResultDashboard() {

  const { interviewId } = useParams();
  const navigate = useNavigate();

  const [result, setResult] = useState(null);

  useEffect(() => {

    axios
      .get(`http://127.0.0.1:8000/api/interview/result/${interviewId}`)
      .then(res => setResult(res.data))
      .catch(err => console.error(err));

  }, [interviewId]);



  if (!result) {
    return (
      <div className="flex justify-center items-center h-screen text-white text-xl">
        Loading Interview Results...
      </div>
    );
  }

  const scores = result.scores || {};
  const feedback = result.feedback || {};



  return (

    <PageWrapper>

      <div className="dashboard-container">

        {/* HEADER */}
        <div className="dashboard-header">

          <h1 className="dashboard-title">
            Interview Analytics Dashboard
          </h1>

          <button
            onClick={() => navigate("/home")}
            className="dashboard-home-btn"
          >
            Home
          </button>

        </div>



        {/* SCORE GRID */}
        <div className="dashboard-grid">

          {Object.entries(scores).map(([k, v], index) => {

            if (k === "final") return null;

            return (

              <div
                key={k}
                className="dashboard-card card-animate"
                style={{ animationDelay: `${index * 0.15}s` }}
              >

                <ScoreCard
                  title={k.replace("_", " ").toUpperCase()}
                  value={`${v} / 100`}
                />

                <div className="dashboard-progress">
                  <ProgressBar value={v} max={100} />
                </div>

              </div>

            );

          })}

        </div>



        {/* PER QUESTION FEEDBACK */}
        {Object.keys(feedback).length > 0 &&

          Object.entries(feedback).map(([section, items]) => (

            <div key={section} className="dashboard-section">

              <h2 className="dashboard-section-title">

                {section.replace("_", " ")} Questions

              </h2>

              {items.map((q, i) => (

                <div key={i} className="dashboard-feedback-card">

                  <p className="dashboard-question">
                    Q{i + 1}: {q.question}
                  </p>

                  <p className="dashboard-score">
                    Score: {q.score}/100
                  </p>

                  <p>
                    <b>Strengths:</b>{" "}
                    {q.strengths?.join(", ") || "N/A"}
                  </p>

                  <p>
                    <b>Weaknesses:</b>{" "}
                    {q.weaknesses?.join(", ") || "N/A"}
                  </p>

                  <p>
                    <b>Suggestions:</b>{" "}
                    {q.suggestions?.join(", ") || "N/A"}
                  </p>

                </div>

              ))}

            </div>

          ))

        }



        {/* FINAL RESULT */}
        <div className="dashboard-final-card">

          <h2>Final AI Score</h2>

          <p className="dashboard-final-score">
            {scores.final || 0} / 100
          </p>

          <p className={`dashboard-decision ${
            result.decision === "Selected"
              ? "selected"
              : "rejected"
          }`}>

            {result.decision}

          </p>

        </div>

      </div>

    </PageWrapper>

  );

}