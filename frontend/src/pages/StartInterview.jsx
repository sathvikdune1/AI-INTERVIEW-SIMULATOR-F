import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import PageWrapper from "../components/PageWrapper";

export default function StartInterview() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    mobile: "",
    job_role: "",
    difficulty: "medium",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const startInterview = async () => {
    if (!form.name || !form.email || !form.mobile || !form.job_role) {
      alert("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/api/interview/start",
        new URLSearchParams(form),
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        }
      );

      localStorage.setItem("interview_id", res.data.interview_id);
      navigate("/upload-resume");
    } catch (err) {
      console.error(err);
      alert("Failed to start interview");
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageWrapper>
      <div className="relative min-h-screen flex items-center justify-center text-white overflow-hidden z-10">

        {/* Background glow */}
        <div className="bg-orb blue w-[300px] h-[300px] top-10 left-10 absolute pointer-events-none" />
        <div className="bg-orb purple w-[260px] h-[260px] bottom-10 right-10 absolute pointer-events-none" />

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="glass-card w-[420px] z-10 p-8"
        >
          <h2 className="text-3xl font-bold neon-text text-center mb-6">
            AI Interview Setup
          </h2>

          <label className="text-sm text-blue-300">Full Name</label>
          <input name="name" onChange={handleChange} className="w-full mb-4 p-3 rounded-lg bg-black/40 outline-none" />

          <label className="text-sm text-blue-300">Email</label>
          <input name="email" onChange={handleChange} className="w-full mb-4 p-3 rounded-lg bg-black/40 outline-none" />

          <label className="text-sm text-blue-300">Mobile Number</label>
          <input name="mobile" onChange={handleChange} className="w-full mb-4 p-3 rounded-lg bg-black/40 outline-none" />

          <label className="text-sm text-blue-300">Job Role</label>
          <input name="job_role" onChange={handleChange} className="w-full mb-4 p-3 rounded-lg bg-black/40 outline-none" />

          <label className="text-sm text-blue-300">Difficulty</label>
          <select name="difficulty" onChange={handleChange} className="w-full mb-6 p-3 rounded-lg bg-black/40">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={startInterview}
            disabled={loading}
            className="w-full py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-500 font-bold"
          >
            {loading ? "Starting..." : "Continue →"}
          </motion.button>
        </motion.div>
      </div>
    </PageWrapper>
  );
}
