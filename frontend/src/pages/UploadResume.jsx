import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { motion } from "framer-motion";
import PageWrapper from "../components/PageWrapper";
import robot from "../assets/ai-robot.png";

export default function UploadResume() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) {
      alert("Please select a resume file");
      return;
    }

    const interview_id = localStorage.getItem("interview_id");
    if (!interview_id) {
      alert("Interview session not found. Please restart.");
      return;
    }

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("interview_id", interview_id);
      formData.append("resume", file);

      /* ---------- STEP 1: UPLOAD RESUME ---------- */
      const uploadRes = await axios.post(
        "http://127.0.0.1:8000/api/interview/upload-resume",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          timeout: 30000
        }
      );

      if (uploadRes.status !== 200) {
        throw new Error("Resume upload failed");
      }

      /* ---------- STEP 2: GENERATE QUESTIONS ---------- */
      const genRes = await axios.post(
        "http://127.0.0.1:8000/api/interview/generate-questions",
        new URLSearchParams({ interview_id }),
        { timeout: 30000 }
      );

      if (genRes.status !== 200) {
        throw new Error("Question generation failed");
      }

      /* ---------- SUCCESS ---------- */
      navigate("/interview");

    } catch (err) {
      console.error("Upload error:", err);

      if (err.response) {
        alert(
          err.response.data?.detail ||
          "Server error during resume processing"
        );
      } else if (err.code === "ECONNABORTED") {
        alert("Server timeout. Please try again.");
      } else {
        alert("Network error. Please check backend.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageWrapper>
      <div className="min-h-screen flex items-center justify-center relative overflow-hidden">

        {/* Glow orbs */}
        <div className="bg-orb blue w-[420px] h-[420px] top-20 left-20 absolute" />
        <div className="bg-orb purple w-[360px] h-[360px] bottom-20 right-20 absolute" />

        <div className="flex items-center gap-28 relative z-10">

          {/* Upload Card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="glass-card w-[380px]"
          >
            <h2 className="text-2xl font-bold neon-text text-center mb-6">
              Upload Your Resume
            </h2>

            <input
              type="file"
              accept=".pdf"
              className="w-full mb-5 text-sm text-white"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={upload}
              disabled={loading}
              className="ai-button"
            >
              {loading ? "Processing..." : "Upload & Continue →"}
            </motion.button>
          </motion.div>

          {/* Robot Animation */}
          <motion.div
            animate={{ y: [0, -14, 0] }}
            transition={{
              repeat: Infinity,
              duration: 4,
              ease: "easeInOut"
            }}
            className="hidden lg:block"
          >
            <img
              src={robot}
              alt="AI Assistant"
              className="h-[420px] drop-shadow-[0_0_35px_rgba(56,189,248,0.6)]"
            />
          </motion.div>

        </div>
      </div>
    </PageWrapper>
  );
}
