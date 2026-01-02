import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function CodingCompiler() {
  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(`# Write your code here`);
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);

  const runCode = async () => {
    setRunning(true);
    setOutput("");

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/compiler/run",
        { language, code }
      );
      setOutput(res.data.output);
    } catch (err) {
      setOutput("Execution failed");
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="glass-card mt-8">
      <h2 className="text-xl font-bold neon-text mb-4">
        Coding Question
      </h2>

      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="w-full mb-3 bg-black/40 p-2 rounded"
      >
        <option value="python">Python</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="java">Java</option>
      </select>

      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="w-full h-52 bg-black/50 text-white p-3 rounded font-mono"
      />

      <motion.button
        whileHover={{ scale: 1.05 }}
        onClick={runCode}
        disabled={running}
        className="ai-button mt-4"
      >
        {running ? "Running..." : "Run Code"}
      </motion.button>

      <pre className="mt-4 bg-black/60 p-3 rounded text-green-400 text-sm">
        {output}
      </pre>
    </div>
  );
}
