import { motion } from "framer-motion";

export default function ScoreCard({ title, value, color }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      whileHover={{
        scale: 1.04,
        boxShadow: "0px 20px 40px rgba(0,0,0,0.4)"
      }}
      className="bg-black/60 rounded-xl p-5 shadow-lg border border-gray-700"
    >
      <p className="text-sm text-gray-400 mb-1">{title}</p>

      <motion.p
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
        className={`text-3xl font-bold ${color}`}
      >
        {value}
      </motion.p>
    </motion.div>
  );
}
