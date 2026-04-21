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
        <div className="bg-orb blue w-[420px] h-[420px] top-20 left-20 absolute pointer-events-none" />
        <div className="bg-orb purple w-[360px] h-[360px] bottom-20 right-20 absolute pointer-events-none" />

        <div className="flex items-center gap-28 relative z-10">

          {/* Upload Card */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="glass-card w-[440px] p-8"
          >
            <h2 className="text-3xl font-bold neon-text text-center mb-8">
              Upload Your Resume
            </h2>

            <div className="flex flex-col gap-5">

              <input
                type="file"
                accept=".pdf"
                className="w-full p-3 rounded-lg bg-black/40 border border-white/10 text-sm text-white cursor-pointer hover:border-blue-400 transition"
                onChange={(e) => setFile(e.target.files[0])}
              />

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={upload}
                disabled={loading}
                className="w-full py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500 font-semibold text-white shadow-lg hover:shadow-blue-500/40 transition"
              >
                {loading ? "Processing..." : "Upload & Continue →"}
              </motion.button>

            </div>
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