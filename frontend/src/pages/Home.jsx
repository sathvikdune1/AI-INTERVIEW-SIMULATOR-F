import { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import PageWrapper from "../components/PageWrapper";

export default function Home() {

  const navigate = useNavigate();
  const [interviews, setInterviews] = useState([]);
  const [starting, setStarting] = useState(false);

  useEffect(() => {

    const token = localStorage.getItem("token");

    axios.get("http://127.0.0.1:8000/api/interview/user", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      const data = res.data.interviews || res.data;
      setInterviews(data);
    })
    .catch(err => console.error(err));

  }, []);


  const startInterview = () => {

    setStarting(true);

    setTimeout(() => {
      navigate("/start");
    }, 1200);

  };


  return (

    <PageWrapper>

      <div className="home-layout">

        {/* HERO */}

        <motion.div
          initial={{opacity:0, y:40}}
          animate={{opacity:1, y:0}}
          transition={{duration:0.6}}
          className="hero-card"
        >

          <h1 className="hero-title">
            AI Interview <span>Simulator</span>
          </h1>

          <p className="hero-desc">
            Practice real AI driven interviews and get instant feedback.
          </p>

          <motion.button
            whileHover={{scale:1.1}}
            whileTap={{scale:0.95}}
            onClick={startInterview}
            className={`start-btn ${starting ? "magic-btn" : ""}`}
          >
            {starting ? "Let's Begin..." : "Start Interview"}
          </motion.button>

        </motion.div>


        {/* HOW IT WORKS */}

        <h2 className="section-title">
          How The Interview Works
        </h2>

        <div className="features-grid">

          <motion.div whileHover={{y:-5}} className="feature-card">
            Upload Resume
            <p>AI analyzes your experience</p>
          </motion.div>

          <motion.div whileHover={{y:-5}} className="feature-card">
            Smart Questions
            <p>Role based technical questions</p>
          </motion.div>

          <motion.div whileHover={{y:-5}} className="feature-card">
            AI Evaluation
            <p>Answers evaluated instantly</p>
          </motion.div>

          <motion.div whileHover={{y:-5}} className="feature-card">
            Performance Report
            <p>Score and improvement tips</p>
          </motion.div>

        </div>


        {/* 🔥 NEW SECTION ADDED (DO NOT MODIFY ABOVE CODE) */}

        <div className="mt-16 px-2">

          <h2 className="section-title">
             Premium Interview Prep Kit
          </h2>

          <p className="text-gray-400 mb-6">
            Not sure where to start? Begin with our curated interview resources.
          </p>

          <motion.div
            whileHover={{ scale: 1.02 }}
            className="feature-card"
            style={{ padding: "30px" }}
          >

            <h3 style={{ fontSize: "20px", marginBottom: "10px" }}>
               Complete Interview Preparation Bundle
            </h3>

            <p className="text-gray-400 mb-4">
              Access coding and technical interview questions 
              carefully curated to help you crack top company interviews.
            </p>

            <a
              href="https://drive.google.com/drive/folders/13Z0kHhwkUR1Iz7CGGB3SWumMpyV9Tmaj?usp=sharing"
              target="_blank"
              rel="noopener noreferrer"
              className="result-btn"
              style={{ display: "inline-block", textAlign: "center" }}
            >
              Explore Resources →
            </a>

          </motion.div>

        </div>


        {/* INTERVIEW LOGS */}

        <h2 className="section-title">
          Interview Logs
        </h2>

        {interviews.length === 0 ? (

          <p className="text-gray-400">
            No interviews completed yet.
          </p>

        ) : (

          <div className="logs-grid">

            {interviews.map((i, index) => (

              <motion.div
                key={i._id || index}

                initial={{opacity:0, y:20}}
                animate={{opacity:1, y:0}}

                transition={{delay:index * 0.05}}

                whileHover={{
                  scale:1.04,
                  rotateX:2,
                  rotateY:2
                }}

                className="log-card"
              >

                <div className="log-content">

                  <h3 className="log-role">
                    {i.role || "Interview"}
                  </h3>

                  <p className="log-score">
                    Score:
                    <span>
                      {i.score ?? 0}/100
                    </span>
                  </p>

                  <p className="log-date">
                    {i.created_at
                      ? new Date(i.created_at).toLocaleDateString()
                      : "Recent"}
                  </p>

                </div>

                <button
                  type="button"
                  onClick={() => navigate(`/result/${i._id}`)}
                  className="result-btn"
                  style={{display:"block"}}
                >
                  View Result
                </button>

              </motion.div>

            ))}

          </div>

        )}

      </div>

    </PageWrapper>

  );

}